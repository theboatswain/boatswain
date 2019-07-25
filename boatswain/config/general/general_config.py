#  This file is part of Boatswain.
#
#      Boatswain is free software: you can redistribute it and/or modify
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

from PyQt5.QtCore import QCoreApplication

from boatswain.common.models.container import Container
from boatswain.common.models.tag import Tag
from boatswain.common.services import config_service, containers_service
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils.constants import CONTAINER_CONF_CHANGED
from boatswain.config.general.general_config_ui import GeneralAppConfigUi


class GeneralAppConfig:
    _translate = QCoreApplication.translate
    template = 'GeneralAppConfig'
    memory_units = ['MB', 'GB']
    cpu_units = ['CPUs', 'Period', 'Quota']

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = GeneralAppConfigUi(parent, container, self)

        for unit in self.memory_units:
            self.ui.memory_unit.addItem(self._translate(self.template, unit))

        for unit in self.cpu_units:
            self.ui.cpu_unit.addItem(self._translate(self.template, unit))

        self.retranslateUi()
        self.loadTags()

        self.ui.sync.clicked.connect(self.onSyncClicked)
        self.ui.container_name.textChanged.connect(self.onNameChanged)
        self.ui.image_tags.currentIndexChanged.connect(self.onImageTagChange)

    def retranslateUi(self):
        self.ui.container_name.setText(self._translate(self.template, self.container.name))
        self.ui.repo_source.setText(self._translate(self.template, "Repo source:     Dockerhub"))
        self.ui.sync.setText(self._translate(self.template, "Sync"))
        self.ui.img_tag_label.setText(self._translate(self.template, "Image tag:"))
        self.ui.limit_cpu_label.setText(self._translate(self.template, "CPU limit:"))
        self.ui.entrypoint_label.setText(self._translate(self.template, "Entrypoint"))
        self.ui.entrypoint.setPlaceholderText(
            self._translate(self.template, "Override the default command of the container"))
        self.ui.limit_memory_label.setText(self._translate(self.template, "Memory limit:   "))
        self.ui.start_with_boatswain.setText(self._translate(self.template, " Start with Boatswain"))
        self.ui.stop_with_boatswain.setText(self._translate(self.template, " Stop when Boatswain exit"))
        self.ui.container_id.setText(self._translate(self.template, "Container ID:     " + self.container.container_id))

    def onSyncClicked(self):
        self.ui.sync.setText(self._translate(self.template, "Syncing"))
        worker = Worker(containers_service.updateContainerTags, self.container)
        worker.signals.result.connect(lambda: self.ui.sync.setText(self._translate(self.template, "Sync")))
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

    def onImageTagChange(self, index):
        if index > 0:
            tag = self.ui.image_tags.itemText(index).split(':')[1]
            self.container.tag = tag
            self.container.save()
            config_service.setAppConf(self.container, CONTAINER_CONF_CHANGED, 'true')
            containers_service.fire(self.container, 'tag_index', index)
