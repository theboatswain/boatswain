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

from PyQt5.QtCore import QMetaObject, QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QWidget, QSizePolicy, QPushButton, QLabel, QComboBox, QFrame, QVBoxLayout, \
    QHBoxLayout, QDialog

from boatswain.common.models.container import Container
from boatswain.common.models.tag import Tag
from boatswain.common.services import config_service
from boatswain.common.utils.constants import CONTAINER_CONF_CHANGED
from boatswain.common.utils.custom_ui import BQSizePolicy, ReloadableWidget
from boatswain.config.app_config import AppConfig


class AdvancedAppWidget(ReloadableWidget):

    def reloadData(self):
        for index, tag in enumerate(Tag.select().where(Tag.container == self.container)):
            self.tags.addItem(self.container.image_name + ":" + tag.name)
            if tag.name == self.container.tag:
                self.tags.setCurrentIndex(index)

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 3, 0)
        self.layout.setSpacing(6)
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)
        self.widget = QWidget(self)
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(6)
        self.label = QLabel(self.widget)
        self.horizontal_layout.addWidget(self.label)
        self.tags = QComboBox(self.widget)
        self.tags.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.tags.setObjectName("tags")
        self.horizontal_layout.addWidget(self.tags)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.widget_2)
        self.layout.addWidget(self.widget)
        self.widget_3 = QWidget(self)
        self.horizontal_layout_2 = QHBoxLayout(self.widget_3)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(6)
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout_2.addWidget(self.widget_4)
        self.advanced_configuration = QPushButton(self.widget_3)
        self.advanced_configuration.setObjectName("advancedConfiguration")
        self.horizontal_layout_2.addWidget(self.advanced_configuration)
        self.layout.addWidget(self.widget_3)

        self.retranslateUi()
        self.reloadData()

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.label.setText(_translate("AdvancedWidget", "Image tag:"))
        self.advanced_configuration.setText(_translate("AdvancedWidget", "Advanced configuration"))

    @pyqtSlot(int, name='on_tags_currentIndexChanged')
    def onImageTagChange(self, index):
        tag = self.tags.itemText(index).split(':')[1]
        self.container.tag = tag
        self.container.update()
        config_service.setAppConf(self.container, CONTAINER_CONF_CHANGED, 'true')
        # Todo: Should we do the clean up? delete the downloaded image

    @pyqtSlot(bool, name='on_advancedConfiguration_clicked')
    def onAdvancedConfigurationClicked(self, checked=True):
        dialog = QDialog()
        dialog.ui = AppConfig("%s - configuration" % self.container.name, dialog, self.container)
        dialog.exec_()
        self.parentWidget().reloadData()