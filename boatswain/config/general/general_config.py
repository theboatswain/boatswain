#  This file is part of Boatswain.
#
#      Boatswain<https://github.com/theboatswain> is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Boatswain is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#
from PyQt5.QtCore import QCoreApplication, QThread

from boatswain.common.models.container import Container
from boatswain.common.models.tag import Tag
from boatswain.common.services import containers_service, auditing_service
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils import utils
from boatswain.config.general.general_config_ui import GeneralAppConfigUi


class GeneralAppConfig:
    _tr = QCoreApplication.translate
    template = 'GeneralAppConfig'

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = GeneralAppConfigUi(parent, container, self)

        self.ui.limit_memory.setMinimum(0)
        self.ui.limit_memory.setMaximum(utils.getPhysicalMemory() * 70 / 100)
        self.ui.limit_memory.setValue(self.container.memory_limit)
        self.ui.limit_memory.sliderReleased.connect(self.onMemoryChanged)
        self.ui.limit_memory.valueChanged.connect(self.onMemoryChanging)
        self.onMemoryChanging()

        self.ui.limit_cpu.setMinimum(0)
        self.ui.limit_cpu.setMaximum(int(QThread.idealThreadCount()) * 100 * 80 / 100)
        self.ui.limit_cpu.setValue(self.container.cpu_limit * 100)
        self.ui.limit_cpu.sliderReleased.connect(self.onCpuChanged)
        self.ui.limit_cpu.valueChanged.connect(self.onCpuChanging)
        self.onCpuChanging()

        self.retranslateUi()
        self.loadTags()

        self.ui.sync.clicked.connect(self.onSyncClicked)
        self.ui.container_name.textChanged.connect(self.onNameChanged)
        self.ui.image_tags.currentIndexChanged.connect(self.onImageTagChange)
        self.ui.entrypoint.textChanged.connect(self.onEntrypointChanged)
        self.ui.entrypoint.setText(container.entrypoint)

    def retranslateUi(self):
        self.ui.container_name.setText(self._tr(self.template, self.container.name))
        self.ui.repo_source.setText(self._tr(self.template, "Repo source:     " + self.container.repo.title()))
        self.ui.sync.setText(self._tr(self.template, "Sync"))
        self.ui.img_tag_label.setText(self._tr(self.template, "Image tag:"))
        self.ui.limit_cpu_label.setText(self._tr(self.template, "CPU limit:"))
        self.ui.entrypoint_label.setText(self._tr(self.template, "Entrypoint"))
        self.ui.entrypoint.setPlaceholderText(
            self._tr(self.template, "Override the default entrypoint of the container"))
        self.ui.limit_memory_label.setText(self._tr(self.template, "Memory limit:   "))
        self.ui.start_with_boatswain.setText(self._tr(self.template, " Start with Boatswain"))
        self.ui.stop_with_boatswain.setText(self._tr(self.template, " Stop when Boatswain exits"))
        self.ui.container_id.setText(self._tr(self.template, "Container ID:     " + self.container.container_id))

    def onSyncClicked(self):
        self.ui.sync.setText(self._tr(self.template, "Syncing"))
        worker = Worker(containers_service.updateContainerTags, self.container)
        worker.signals.result.connect(lambda: self.ui.sync.setText(self._tr(self.template, "Sync")))
        worker.signals.finished.connect(self.loadTags)
        threadpool.start(worker)

    def loadTags(self):
        self.ui.image_tags.clear()
        for index, tag in enumerate(Tag.select().where(Tag.container == self.container)):
            self.ui.image_tags.addItem(self.container.image_name + ":" + tag.name)
            if tag.name == self.container.tag:
                self.ui.image_tags.setCurrentIndex(index)

    def onNameChanged(self, name):
        if len(name) == 0:
            self.container.name = self.container.image_name
        else:
            self.container.name = name
        containers_service.fire(self.container, 'name', name)
        self.container.save()

    def onEntrypointChanged(self, entrypoint):
        previous_entrypoint = self.container.entrypoint
        self.container.entrypoint = entrypoint
        self.container.save()
        auditing_service.audit_update(self.container, self.container.tableName(),
                                      self.container.id, "entrypoint", previous_entrypoint, entrypoint)

    def onImageTagChange(self, index):
        if index > 0:
            tag = self.ui.image_tags.itemText(index).split(':')[1]
            previous_tag = self.container.tag
            self.container.tag = tag
            self.container.save()
            auditing_service.audit_update(self.container, self.container.tableName(),
                                          self.container.id, "tag", previous_tag, tag)
            containers_service.fire(self.container, 'tag_index', index)

    def onMemoryChanged(self):
        previous_memory_limit = self.container.memory_limit
        self.container.memory_limit = self.ui.limit_memory.value()
        self.container.save()
        auditing_service.audit_update(self.container, self.container.tableName(), self.container.id,
                                      "memory_limit", previous_memory_limit, self.container.memory_limit)

    def onCpuChanged(self):
        previous_cpu_limit = self.container.cpu_limit
        self.container.cpu_limit = self.ui.limit_cpu.value() / 100.0
        self.container.save()
        auditing_service.audit_update(self.container, self.container.tableName(), self.container.id,
                                      "cpu_limit", previous_cpu_limit, self.container.cpu_limit)

    def onCpuChanging(self):
        if self.ui.limit_cpu.value() > 0:
            self.ui.current_n_cpus.setText(str(self.ui.limit_cpu.value() / 100.0) + " CPUs")
        else:
            self.ui.current_n_cpus.setText(self._tr(self.template, "Unlimited"))

    def onMemoryChanging(self):
        if self.ui.limit_memory.value() > 0:
            self.ui.current_n_memory.setText(str(self.ui.limit_memory.value()) + " MB")
        else:
            self.ui.current_n_memory.setText(self._tr(self.template, "Unlimited"))
