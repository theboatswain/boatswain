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

from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QDialog

from boatswain.common.models.container import Container
from boatswain.common.models.tag import Tag
from boatswain.common.services import config_service, containers_service
from boatswain.common.utils.constants import CONTAINER_CONF_CHANGED
from boatswain.config.app_config import AppConfig
from boatswain.home.advanced.advanced_widget_ui import AdvancedAppWidgetUi


class AdvancedAppWidget:

    animation: QPropertyAnimation

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = AdvancedAppWidgetUi(parent, container)
        self.ui.advanced_configuration.clicked.connect(self.onAdvancedConfigurationClicked)
        self.ui.tags.currentIndexChanged.connect(self.onImageTagChange)
        self.app_info_max_height = self.ui.sizeHint().height() + 10
        self.ui.setMaximumHeight(0)
        containers_service.listenContainerChange(container, self.onContainerChange)
        self.onContainerChange()

    def onImageTagChange(self, index):
        tag = self.ui.tags.itemText(index).split(':')[1]
        self.container.tag = tag
        self.container.update()
        config_service.setAppConf(self.container, CONTAINER_CONF_CHANGED, 'true')
        # Todo: Should we do the clean up? delete the downloaded image

    def onAdvancedConfigurationClicked(self):
        dialog = QDialog(self.ui)
        dialog.ui = AppConfig("%s - configuration" % self.container.name, dialog, self.container)
        dialog.exec_()

    def toggleWindow(self):
        if self.ui.maximumHeight() == 0:
            self.animation = QPropertyAnimation(self.ui, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.app_info_max_height)
            self.animation.start()
        else:
            self.animation = QPropertyAnimation(self.ui, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setStartValue(self.app_info_max_height)
            self.animation.setEndValue(0)
            self.animation.start()

    def onContainerChange(self):
        self.ui.tags.clear()
        for index, tag in enumerate(Tag.select().where(Tag.container == self.container)):
            self.ui.tags.addItem(self.container.image_name + ":" + tag.name)
            if tag.name == self.container.tag:
                self.ui.tags.setCurrentIndex(index)