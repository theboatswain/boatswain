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

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QDialog

from boatswain.common.models.container import Container
from boatswain.config.app_config_ui import AppConfigUi


class AppConfig:

    _translate = QCoreApplication.translate
    template = 'AppConfig'

    def __init__(self, parent, container: Container) -> None:
        self.container = container

        self.dialog = QDialog(parent)

        self.dialog = self.dialog
        self.ui = AppConfigUi(self.dialog, container)
        self.dialog.ui = self.ui

        self.retranslateUi()
        self.ui.tab_widget.setCurrentIndex(0)
        self.ui.tab_widget.currentChanged.connect(self.onTabChange)

        self.dialog.setWindowTitle("%s - configuration" % self.container.name)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)

    def retranslateUi(self):
        general_tab_name = self._translate(self.template, "General")
        self.ui.tab_widget.setTabText(self.ui.tab_widget.indexOf(self.ui.general), general_tab_name)
        port_tab_name = self._translate(self.template, "Port mapping")
        self.ui.tab_widget.setTabText(self.ui.tab_widget.indexOf(self.ui.port), port_tab_name)
        volume_tab_name = self._translate(self.template, "Volume mount")
        self.ui.tab_widget.setTabText(self.ui.tab_widget.indexOf(self.ui.volume), volume_tab_name)
        environment_tab_name = self._translate(self.template, "Environment")
        self.ui.tab_widget.setTabText(self.ui.tab_widget.indexOf(self.ui.environment.ui), environment_tab_name)

    def onTabChange(self, index):
        widget = self.ui.tab_widget.widget(index)
        self.dialog.setMinimumSize(widget.preferableSize())
        self.dialog.resize(widget.preferableSize())
        # prevWidget = self.tab_widget.currentWidget()
        # self.animation = QPropertyAnimation(self.dialog, b"maximumSize")
        # self.animation.setDuration(300)
        # self.animation.setStartValue(prevWidget.preferableSize())
        # self.animation.setEndValue(widget.preferableSize())
        # self.animation.start()

    def show(self):
        self.dialog.exec_()
