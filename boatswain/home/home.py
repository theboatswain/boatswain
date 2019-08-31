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
from typing import Dict

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QWidget
from boatswain.common.models.group import Group
from boatswain_updater.utils import sys_utils
from playhouse.shortcuts import update_model_from_dict, model_to_dict

from boatswain.about.about import AboutDialog
from boatswain.common.exceptions.workspace import WorkspaceAlreadyExistsException
from boatswain.common.models.container import Container
from boatswain.common.services import data_transporter_service, global_preference_service, workspace_service, \
    group_service, containers_service
from boatswain.common.services.system_service import rt
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils import message_utils
from boatswain.common.utils.constants import CONTAINER_CHANNEL, ADD_APP_CHANNEL, UPDATES_CHANNEL
from boatswain.home.application.application_widget import AppWidget
from boatswain.home.application.application_widget_ui import AppWidgetUi
from boatswain.home.group.group_widget import GroupWidget
from boatswain.home.group.group_widget_ui import GroupWidgetUi
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
        self.apps: Dict[int, AppWidgetUi] = {}
        self.groups: Dict[int, GroupWidgetUi] = {}

        if sys_utils.isWin():
            self.ui.menu_bar.hide()

        self.loadWorkspaces()

        self.ui.workspaces.on_option_selected.connect(self.onWorkspaceChanged)
        data_transporter_service.listen(CONTAINER_CHANNEL, self.addAppFromContainer)
        data_transporter_service.listen(ADD_APP_CHANNEL, self.addAppClicked)
        self.ui.resizeEvent = self.resizeEvent
        self.ui.search_app.textChanged.connect(self.search)
        self.ui.about.triggered.connect(self.showAbout)
        self.ui.check_for_update.triggered.connect(lambda: data_transporter_service.fire(UPDATES_CHANNEL, False))

        self.loadApps()

    def loadApps(self):
        groups = group_service.getGroups()
        for group in groups:
            self.addGroupWidget(group)
        for container in containers_service.getAllContainer():
            self.addAppFromContainer(container)

    def addAppClicked(self, group=None):
        dialog = SearchAppDialog(self._tr("Add app"), self.ui, group)
        dialog.show()

    def _tr(self, message):
        return self._translate(self.tpl, message)

    def loadWorkspaces(self):
        self.ui.workspaces.clear()
        self.ui.workspaces.addItem(self._tr('All'), self._tr('All workspaces'), separate_after=True)
        for workspace in workspace_service.getWorkspaces():
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
                message_utils.error(self._tr('Workspace already exists'),
                                    self._tr('Please choose a different workspace\'s name'))

    def addGroupWidget(self, group: Group):
        group_widget = GroupWidget(group, self.ui.app_list)
        group_widget.move_app.connect(self.moveAppToGroup)
        group_widget.move_group.connect(self.moveGroup)
        self.groups[group.id] = group_widget.ui
        self.ui.app_list.layout().addWidget(group_widget.ui)

    def addAppFromContainer(self, container: Container):
        current_workspace = self.ui.workspaces.getCurrentOption()
        widget = AppWidget(self.ui.app_list, container)
        widget.move_app.connect(self.moveWidget)
        widget.new_group.connect(self.createGroup)
        self.apps[container.id] = widget.ui
        if container.group.id not in self.groups:
            self.addGroupWidget(container.group)
        if current_workspace != 'All':
            if container.group.workspace.name != current_workspace:
                self.groups[container.group.id].hide()
        self.groups[container.group.id].app_list_layout.addWidget(widget.ui)

    def show(self):
        self.ui.show()

    # def updateApps(self):
    #     self.apps.clear()
    #     for i in reversed(range(self.ui.app_list_layout.count())):
    #         self.ui.app_list_layout.itemAt(i).widget().setParent(None)
    #     for container in containers_service.getAllContainer():
    #         self.addAppFromContainer(container)

    def moveWidget(self, container, widget: AppWidgetUi):
        widget_to_be_moved = self.apps[container.id]

        # Update the in-memory object of container
        update_model_from_dict(widget_to_be_moved.container, model_to_dict(container))
        widget_to_be_moved.parentWidget().layout().removeWidget(widget_to_be_moved)
        index = widget.parentWidget().layout().indexOf(widget)
        widget.parentWidget().layout().insertWidget(index + 1, widget_to_be_moved)

    def moveAppToGroup(self, container, widget: GroupWidgetUi):
        widget_to_be_moved = self.apps[container.id]

        # Update the in-memory object of container
        update_model_from_dict(widget_to_be_moved.container, model_to_dict(container))
        widget_to_be_moved.parentWidget().layout().removeWidget(widget_to_be_moved)
        widget.app_list_layout.addWidget(widget_to_be_moved)

    def moveGroup(self, group: Group, widget: GroupWidgetUi):
        group_to_be_moved: GroupWidgetUi = self.groups[group.id]
        update_model_from_dict(group_to_be_moved.group, model_to_dict(group))
        group_to_be_moved.parentWidget().layout().removeWidget(group_to_be_moved)
        index = widget.parentWidget().layout().indexOf(widget)
        widget.parentWidget().layout().insertWidget(index + 1, group_to_be_moved)

    def createGroup(self, container, widget: AppWidgetUi):
        widget_to_be_moved = self.apps[container.id]
        # Update the in-memory object of container
        update_model_from_dict(widget_to_be_moved.container, model_to_dict(container))
        group = group_service.createGroup(self._tr('New Folder'))
        widget_to_be_moved.container.group = group
        widget_to_be_moved.container.save()
        widget.container.group = group
        widget.container.save()
        group_widget = GroupWidget(group, self.ui.app_list)
        self.groups[group.id] = group_widget.ui
        self.ui.app_list.layout().addWidget(group_widget.ui)
        widget_to_be_moved.parentWidget().layout().removeWidget(widget_to_be_moved)
        group_widget.ui.app_list_layout.addWidget(widget_to_be_moved)
        widget.parentWidget().layout().removeWidget(widget)
        group_widget.ui.app_list_layout.addWidget(widget)

    def onWorkspaceChanged(self, workspace_name: str):
        workspace_service.activeWorkspace(workspace_name)
        self.search(workspace=workspace_name)

    def search(self, data=None, workspace=None):
        filter_by = self.ui.workspaces.getCurrentOption()
        if workspace is not None:
            filter_by = workspace
        keyword = self.ui.search_app.text()

        for group in self.groups:
            self.groups[group].show()

        for app in self.apps:
            self.apps[app].show()

        if filter_by != 'All':
            for group in self.groups:
                if self.groups[group].group.workspace.name != filter_by:
                    self.groups[group].hide()

        if not keyword:
            return
        for app in self.apps:
            if keyword not in self.apps[app].container.name and keyword not in self.apps[app].container.image_name:
                self.apps[app].hide()

    def resizeEvent(self, event: QResizeEvent):
        global_preference_service.setHomeWindowSize(event.size())
        QMainWindow.resizeEvent(self.ui, event)

    def showAbout(self):
        about = AboutDialog(self.ui)
        about.show()
