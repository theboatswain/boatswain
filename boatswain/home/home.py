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
from idlelib.idle_test.test_help_about import About
from typing import List
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow

from boatswain.about.about import AboutDialog
from boatswain.common.models.container import Container
from boatswain.common.services import data_transporter_service, global_preference_service, containers_service
from boatswain.common.utils.constants import CONTAINER_CHANNEL, ADD_APP_CHANNEL, APP_EXIT_CHANNEL
from boatswain.home.application.application_widget import AppWidget
from boatswain.home.home_ui import HomeUi
from boatswain.search.search_app import SearchAppDialog


class Home:
    """ Home screen """

    filters = ['All apps', 'Running', 'Stopped']
    _translate = QCoreApplication.translate
    template = 'Boatswain'

    def __init__(self):
        super(Home, self).__init__()
        self.ui = HomeUi()
        self.ui.resize(global_preference_service.getHomeWindowSize())
        self.ui.setMinimumSize(global_preference_service.getMinimumHomeWindowSize())
        self.ui.add_app.clicked.connect(self.addAppClicked)
        self.ui.action_add.triggered.connect(self.addAppClicked)
        self.apps: List[AppWidget] = []

        for item in self.filters:
            self.ui.app_type.addItem(self._translate(self.template, item))

        data_transporter_service.listen(CONTAINER_CHANNEL, self.addAppFromContainer)
        data_transporter_service.listen(ADD_APP_CHANNEL, self.addAppClicked)
        self.ui.resizeEvent = self.resizeEvent
        self.ui.app_type.currentTextChanged.connect(self.search)
        self.ui.search_app.textChanged.connect(self.search)
        self.ui.about.triggered.connect(self.showAbout)

    def addAppClicked(self):
        dialog = SearchAppDialog("Add app", self.ui)
        dialog.show()

    def addAppFromContainer(self, container: Container):
        widget = AppWidget(self.ui.app_list, container)
        self.apps.append(widget)
        self.ui.app_list.layout().addWidget(widget.ui)

    def show(self):
        self.ui.show()

    def search(self, data=None):
        filter_by = self.ui.app_type.currentText()
        keyword = self.ui.search_app.text()

        for app in self.apps:
            app.ui.show()

        if filter_by == 'Running':
            for app in self.apps:
                if not containers_service.isContainerRunning(app.container):
                    app.ui.hide()
        if filter_by == 'Stopped':
            for app in self.apps:
                if containers_service.isContainerRunning(app.container):
                    app.ui.hide()
        if not keyword:
            return
        for app in self.apps:
            if keyword not in app.container.name and keyword not in app.container.image_name:
                app.ui.hide()

    def resizeEvent(self, event: QResizeEvent):
        global_preference_service.setHomeWindowSize(event.size())
        QMainWindow.resizeEvent(self.ui, event)

    def showAbout(self):
        about = AboutDialog(self.ui)
        about.show()
