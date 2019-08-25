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
from typing import List

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QLineEdit
from boatswain_updater.utils import sys_utils

from boatswain.about.about import AboutDialog
from boatswain.common.exceptions.workspace import WorkspaceAlreadyExistsException
from boatswain.common.models.container import Container
from boatswain.common.services import data_transporter_service, global_preference_service, containers_service, \
    workspace_service
from boatswain.common.services.system_service import rt
from boatswain.common.utils import message_utils
from boatswain.common.utils.constants import CONTAINER_CHANNEL, ADD_APP_CHANNEL, UPDATES_CHANNEL
from boatswain.home.application.application_widget import AppWidget
from boatswain.home.home_ui import HomeUi
from boatswain.search.search_app import SearchAppDialog


class Home:
    """ Home screen """

    _translate = QCoreApplication.translate
    tpl = 'Boatswain'

    def __init__(self):
        super(Home, self).__init__()
        self.ui = HomeUi()
        self.ui.resize(global_preference_service.getHomeWindowSize())
        self.ui.setMinimumSize(global_preference_service.getMinimumHomeWindowSize())
        self.ui.add_app.clicked.connect(self.addAppClicked)
        self.ui.action_add.triggered.connect(self.addAppClicked)
        self.apps: List[AppWidget] = []

        if sys_utils.isWin():
            self.ui.menu_bar.hide()

        self.loadWorkspaces()

        self.ui.workspaces.onOptionSelected.connect(self.onWorkspaceChanged)
        data_transporter_service.listen(CONTAINER_CHANNEL, self.addAppFromContainer)
        data_transporter_service.listen(ADD_APP_CHANNEL, self.addAppClicked)
        self.ui.resizeEvent = self.resizeEvent
        self.ui.search_app.textChanged.connect(self.search)
        self.ui.about.triggered.connect(self.showAbout)
        self.ui.check_for_update.triggered.connect(lambda: data_transporter_service.fire(UPDATES_CHANNEL, False))

    def addAppClicked(self):
        dialog = SearchAppDialog("Add app", self.ui)
        dialog.show()

    def _tr(self, message):
        return self._translate(self.tpl, message)

    def loadWorkspaces(self):
        self.ui.workspaces.clear()
        self.ui.workspaces.addItem(self._tr('All'), self._tr('All workspaces'), separate_after=True)
        for workspace in workspace_service.getWorkspaces():
            if workspace.name != 'All':
                self.ui.workspaces.addItem(workspace.name)
        self.ui.workspaces.setCurrentOption(workspace_service.getCurrentActivatedWorkspace().name)
        self.ui.workspaces.addItem(self._tr('New'), self._tr('Create a new workspace...'), separate_before=True,
                                   handler=self.newWorkspaceClicked)

    def newWorkspaceClicked(self):
        dlg = QInputDialog(self.ui)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText(self._tr("Workspace name:"))
        dlg.resize(rt(300), rt(100))
        ok = dlg.exec_()
        name = dlg.textValue()
        if ok:
            try:
                workspace = workspace_service.createWorkspace(name)
                self.onWorkspaceChanged(workspace_name=workspace.name)
                self.loadWorkspaces()
            except WorkspaceAlreadyExistsException:
                message_utils.error('Workspace already exists', 'Please choose a different workspace\'s name')

    def addAppFromContainer(self, container: Container):
        widget = AppWidget(self.ui.app_list, container)
        self.apps.append(widget)
        self.ui.app_list.layout().addWidget(widget.ui)
        filter_by = self.ui.workspaces.getCurrentOption()
        if filter_by != 'All':
            if widget.container.group.workspace.name != filter_by:
                widget.ui.hide()

    def show(self):
        self.ui.show()

    def onWorkspaceChanged(self, workspace_name: str):
        workspace_service.activeWorkspace(workspace_name)
        self.search(workspace=workspace_name)

    def search(self, data=None, workspace=None):
        filter_by = self.ui.workspaces.getCurrentOption()
        if workspace is not None:
            filter_by = workspace
        keyword = self.ui.search_app.text()

        for app in self.apps:
            app.ui.show()

        if filter_by != 'All':
            for app in self.apps:
                if app.container.group.workspace.name != filter_by:
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
