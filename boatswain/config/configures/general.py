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
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5.QtCore import QCoreApplication, QMetaObject, Qt, pyqtSlot
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton, QComboBox, QLineEdit, QCheckBox, QWidget, QVBoxLayout, \
    QHBoxLayout, QFrame

from boatswain.common.models.container import Container
from boatswain.common.models.tag import Tag
from boatswain.common.services import config_service, containers_service
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils import text_utils
from boatswain.common.utils.app_avatar import AppAvatar
from boatswain.common.utils.constants import CONTAINER_CONF_CHANGED
from boatswain.common.utils.custom_ui import BQSizePolicy, AutoResizeWidget


class GeneralAppConfig(AutoResizeWidget):

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container        
        self.vertical_layout_2 = QVBoxLayout(self)
        self.vertical_layout_2.setContentsMargins(20, 11, 20, 11)
        self.vertical_layout_2.setSpacing(6)
        self.widget = QWidget(self)
        self.widget.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.horizontal_layout_2 = QHBoxLayout(self.widget)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(6)

        self._translate = QCoreApplication.translate

        img_name = self.container.image_name
        name_part = self.container.image_name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=self, radius=21)

        self.horizontal_layout_2.addWidget(self.pic)
        self.container_name = QLineEdit(self.widget)

        # Remove the border outline on focus
        self.container_name.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.container_name.setStyleSheet('border: none; background-color: transparent')
        self.container_name.setFocusPolicy(Qt.StrongFocus)
        self.container_name.setFocus()
        self.container_name.setObjectName('containerName')
        self.horizontal_layout_2.addWidget(self.container_name)
        self.widget_5 = QWidget(self.widget)
        self.widget_5.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout_2.addWidget(self.widget_5)
        self.vertical_layout_2.addWidget(self.widget)
        self.line_3 = QFrame(self)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.vertical_layout_2.addWidget(self.line_3)
        self.widget_3 = QWidget(self)
        self.widget_3.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.vertical_layout_4 = QVBoxLayout(self.widget_3)
        self.vertical_layout_4.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_4.setSpacing(6)
        self.repo_source = QLabel(self.widget_3)
        self.vertical_layout_4.addWidget(self.repo_source)
        self.container_id = QLabel(self.widget_3)
        self.vertical_layout_4.addWidget(self.container_id)
        self.vertical_layout_2.addWidget(self.widget_3)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.vertical_layout_2.addWidget(self.line)
        self.widget_4 = QWidget(self)
        self.widget_4.setSizePolicy(BQSizePolicy(v_stretch=2))
        self.grid_layout = QGridLayout(self.widget_4)
        self.grid_layout.setContentsMargins(0, 0, 0, 5)
        self.grid_layout.setSpacing(6)
        self.sync = QPushButton(self.widget_4)
        self.sync.setObjectName("sync")
        self.sync.setFocusPolicy(Qt.NoFocus)
        self.grid_layout.addWidget(self.sync, 2, 4, 1, 1)
        self.widget_8 = QWidget(self.widget_4)
        self.widget_8.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.grid_layout.addWidget(self.widget_8, 2, 5, 1, 1)
        self.img_tag_label = QLabel(self.widget_4)
        self.grid_layout.addWidget(self.img_tag_label, 2, 0, 1, 1)
        self.memory_unit = QComboBox(self.widget_4)
        self.memory_unit.setObjectName("memoryUnit")
        self.memory_unit.addItem("")
        self.memory_unit.addItem("")
        self.grid_layout.addWidget(self.memory_unit, 3, 2, 1, 1)
        self.cpu_unit = QComboBox(self.widget_4)
        self.cpu_unit.setObjectName("cpuUnit")
        self.cpu_unit.addItem("")
        self.cpu_unit.addItem("")
        self.cpu_unit.addItem("")
        self.grid_layout.addWidget(self.cpu_unit, 4, 2, 1, 1)
        self.widget_7 = QWidget(self.widget_4)
        self.widget_7.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.grid_layout.addWidget(self.widget_7, 3, 3, 1, 1)
        self.limit_cpu_label = QLabel(self.widget_4)
        self.grid_layout.addWidget(self.limit_cpu_label, 4, 0, 1, 1)
        self.entrypoint_label = QLabel(self.widget_4)
        self.grid_layout.addWidget(self.entrypoint_label, 5, 0, 1, 1)
        self.image_tags = QComboBox(self.widget_4)
        self.image_tags.setObjectName("imageTags")
        self.grid_layout.addWidget(self.image_tags, 2, 1, 1, 3)
        self.limit_memory_label = QLabel(self.widget_4)
        self.grid_layout.addWidget(self.limit_memory_label, 3, 0, 1, 1)
        self.limit_memory = QLineEdit(self.widget_4)
        self.limit_memory.setFocusPolicy(Qt.ClickFocus)
        self.limit_memory.setObjectName("limitMemory")
        self.limit_memory.setText(str(self.container.memory_limit))
        self.limit_memory.setValidator(QIntValidator(0, 9999999))
        self.grid_layout.addWidget(self.limit_memory, 3, 1, 1, 1)
        self.limit_cpu = QLineEdit(self.widget_4)
        self.limit_cpu.setFocusPolicy(Qt.ClickFocus)
        self.limit_cpu.setObjectName("limitCpu")
        self.limit_cpu.setText(str(self.container.cpu_limit))
        self.limit_cpu.setValidator(QDoubleValidator(0, 99999999, 2))
        self.grid_layout.addWidget(self.limit_cpu, 4, 1, 1, 1)
        self.entrypoint = QLineEdit(self.widget_4)
        self.entrypoint.setFocusPolicy(Qt.ClickFocus)
        self.grid_layout.addWidget(self.entrypoint, 5, 1, 1, 3)
        self.vertical_layout_2.addWidget(self.widget_4)
        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.vertical_layout_2.addWidget(self.line_2)
        self.widget_2 = QWidget(self)
        self.widget_2.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.vertical_layout_3 = QVBoxLayout(self.widget_2)
        self.vertical_layout_3.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_3.setSpacing(6)
        self.start_with_boatswain = QCheckBox(self.widget_2)
        self.start_with_boatswain.setObjectName("startWith")
        self.vertical_layout_3.addWidget(self.start_with_boatswain)
        self.stop_with_boatswain = QCheckBox(self.widget_2)
        self.stop_with_boatswain.setObjectName("stopWith")
        self.vertical_layout_3.addWidget(self.stop_with_boatswain)
        self.vertical_layout_2.addWidget(self.widget_2)

        self.retranslateUi()
        self.loadTags()
        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.container_name.setText(self._translate("General", self.container.name))
        self.repo_source.setText(self._translate("General", "Repo source:     Dockerhub"))
        self.container_id.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.sync.setText(self._translate("General", "Sync"))
        self.img_tag_label.setText(self._translate("General", "Image tag:"))
        self.memory_unit.setItemText(0, self._translate("General", "MB"))
        self.memory_unit.setItemText(1, self._translate("General", "GB"))
        self.cpu_unit.setItemText(0, self._translate("General", "CPUs"))
        self.cpu_unit.setItemText(1, self._translate("General", "Period"))
        self.cpu_unit.setItemText(2, self._translate("General", "Quota"))
        self.limit_cpu_label.setText(self._translate("General", "CPU limit:"))
        self.entrypoint_label.setText(self._translate("General", "Entrypoint"))
        self.entrypoint.setPlaceholderText(self._translate("General", "Override the default command of the container"))
        self.limit_memory_label.setText(self._translate("General", "Memory limit:   "))
        self.start_with_boatswain.setText(self._translate("General", " Start with Boatswain"))
        self.stop_with_boatswain.setText(self._translate("General", " Stop when Boatswain exit"))

    @pyqtSlot(bool, name='on_sync_clicked')
    def onSyncClicked(self):
        self.sync.setText(self._translate("General", "Syncing"))
        worker = Worker(containers_service.updateContainerTags, self.container)
        worker.signals.result.connect(lambda: self.sync.setText(self._translate("General", "Sync")))
        worker.signals.finished.connect(self.loadTags)
        threadpool.start(worker)

    def loadTags(self):
        self.image_tags.clear()
        for index, tag in enumerate(Tag.select().where(Tag.container == self.container)):
            self.image_tags.addItem(self.container.image_name + ":" + tag.name)
            if tag.name == self.container.tag:
                self.image_tags.setCurrentIndex(index)

    @pyqtSlot(str, name='on_containerName_textChanged')
    def onNameChanged(self, name):
        if len(name) == 0:
            self.container.name = self.container.image_name
        else:
            self.container.name = name
        self.container.save()

    @pyqtSlot(int, name='on_imageTags_currentIndexChanged')
    def onImageTagChange(self, index):
        tag = self.image_tags.itemText(index).split(':')[1]
        self.container.tag = tag
        self.container.save()
        config_service.setAppConf(self.container, CONTAINER_CONF_CHANGED, 'true')

    def showEvent(self, QShowEvent):
        super().showEvent(QShowEvent)
        container_id = self.container.container_id
        if container_id == '':
            container_id = 'Not available'
        self.container_id.setText(self._translate("General", "Container ID:     " + container_id))


