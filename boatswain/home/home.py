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
from PyQt5.QtCore import QCoreApplication

from boatswain.common.models.container import Container
from boatswain.common.services import data_transporter_service
from boatswain.common.utils.constants import CONTAINER_CHANNEL, ADD_APP_CHANNEL
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

        self.ui.add_app.clicked.connect(self.addAppClicked)
        self.ui.action_add.triggered.connect(self.addAppClicked)

        for item in self.filters:
            self.ui.app_type.addItem(self._translate(self.template, item))

        data_transporter_service.listen(CONTAINER_CHANNEL, self.addAppFromContainer)
        data_transporter_service.listen(ADD_APP_CHANNEL, self.addAppClicked)

    def addAppClicked(self):
        dialog = SearchAppDialog("Add app", self.ui)
        dialog.show()

    def addAppFromContainer(self, container: Container):
        widget = AppWidget(self.ui.app_list, container)
        self.ui.app_list.layout().addWidget(widget.ui)

    def show(self):
        self.ui.show()
