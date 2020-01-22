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
from typing import Dict

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QInputDialog, QMenu, QAction, QMessageBox
from boatswain_updater.utils import sys_utils
from playhouse.shortcuts import update_model_from_dict, model_to_dict

from boatswain.about.about import AboutDialog
from boatswain.common.exceptions.workspace import WorkspaceAlreadyExistsException
from boatswain.common.models.container import Container
from boatswain.common.models.group import Group
from boatswain.common.services import data_transporter_service, global_preference_service, workspace_service, \
    group_service, containers_service, docker_service, boatswain_daemon
from boatswain.common.services.system_service import rt
from boatswain.common.utils import message_utils, utils
from boatswain.common.utils.constants import CONTAINER_CHANNEL, ADD_APP_CHANNEL, UPDATES_CHANNEL, APP_EXIT_CHANNEL, \
    WORKSPACE_CHANGED_CHANNEL, DELETE_GROUP_CHANNEL, PERFORMING_SEARCH_CHANNEL
from boatswain.common.utils.utils import tr
from boatswain.connection.connection_management import ConnectionManagement
from boatswain.home.application.application_widget import AppWidget
from boatswain.home.application.application_widget_ui import AppWidgetUi
from boatswain.home.group.group_widget import GroupWidget
from boatswain.home.group.group_widget_ui import GroupWidgetUi
from boatswain.home.home_ui import HomeUi
from boatswain.preferences.global_preferences import GlobalPreferences
from boatswain.search.search_app import SearchAppDialog


class Home:
    """ Home screen """

    def __init__(self):
        super(Home, self).__init__()
        self.ui = HomeUi()
        self.ui.resize(global_preference_service.getHomeWindowSize())
        self.ui.setMinimumSize(global_preference_service.getMinimumHomeWindowSize())
        self.ui.add_app.clicked.connect(self.addAppClicked)
        data_transporter_service.listen(CONTAINER_CHANNEL, self.addAppFromContainer)
        data_transporter_service.listen(ADD_APP_CHANNEL, self.addAppClicked)
        data_transporter_service.listen(WORKSPACE_CHANGED_CHANNEL, self.loadWorkspaces)
        data_transporter_service.listen(DELETE_GROUP_CHANNEL, self.deleteGroup)
        data_transporter_service.listen(PERFORMING_SEARCH_CHANNEL, self.search)
        self.apps: Dict[int, AppWidgetUi] = {}
        self.groups: Dict[int, GroupWidgetUi] = {}
        self.ui.workspaces.on_option_selected.connect(self.onWorkspaceChanged)
        self.ui.resizeEvent = self.resizeEvent
        self.ui.search_app.textChanged.connect(self.search)
        self.ui.custom_menu.clicked.connect(self.onMenuClicked)

        # Create daemon to listen to docker events
        self.daemon = boatswain_daemon.BoatswainDaemon(self.ui)

        if not sys_utils.isMac():
            self.ui.menu_bar.hide()

        if not docker_service.isDockerRunning():
            connection = ConnectionManagement()
            connection.conf_updated.connect(self.initialise)
            connection.show()
        else:
            self.initialise()

    def initialise(self):
        self.loadWorkspaces()
        self.loadGroups()

        self.daemon.start()
        data_transporter_service.listen(APP_EXIT_CHANNEL, lambda: self.daemon.events.close())

    def loadGroups(self):
        groups = group_service.getGroups()
        for group in groups:
            self.addGroupWidget(group)
        for container in containers_service.getAllContainer():
            self.addAppFromContainer(container)

    def addAppClicked(self, group=None):
        dialog = SearchAppDialog(tr("Add app"), None, group)
        dialog.show()

    def loadWorkspaces(self):
        self.ui.workspaces.clear()
        default = workspace_service.getDefaultWorkspace()
        self.ui.workspaces.addItem(default.id, tr(default.name), tr('All workspaces'), separate_after=True)
        for workspace in workspace_service.getWorkspaces():
            self.ui.workspaces.addItem(workspace.id, workspace.name)
        self.ui.workspaces.setCurrentOption(workspace_service.getCurrentActivatedWorkspace().id)
        self.ui.workspaces.addItem(tr('New'), tr('Create a new workspace...'), separate_before=True,
                                   handler=self.newWorkspaceClicked)

    def newWorkspaceClicked(self):
        dlg = QInputDialog(None)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText(tr("Workspace name:"))
        dlg.resize(rt(300), rt(100))
        ok = dlg.exec_()
        name = dlg.textValue()
        if ok:
            try:
                workspace = workspace_service.createWorkspace(name)
                self.onWorkspaceChanged(workspace_id=workspace.id)
                self.loadWorkspaces()
            except WorkspaceAlreadyExistsException:
                message_utils.error(tr('Workspace already exists'),
                                    tr('Please choose a different name for your workspace'))

    def addGroupWidget(self, group: Group):
        group_widget = GroupWidget(group, self.ui.app_list)
        group_widget.move_app.connect(self.moveAppToGroup)
        group_widget.move_group.connect(self.moveGroup)
        group_widget.delete_group.connect(self.deleteGroup)
        self.groups[group.id] = group_widget.ui
        self.ui.app_list.layout().addWidget(group_widget.ui)

    def addAppFromContainer(self, container: Container):
        current_workspace = self.ui.workspaces.getCurrentOption()
        current_workspace = workspace_service.getWorkspaceById(int(current_workspace))
        if container.group.id not in self.groups:
            self.addGroupWidget(container.group)
        if not current_workspace.is_default:
            if container.group.workspace.id != current_workspace.id:
                self.groups[container.group.id].hide()
        widget = AppWidget(self.groups[container.group.id].app_list, container)
        widget.move_app.connect(self.moveAppWidget)
        widget.new_group.connect(self.createGroup)
        widget.delete_app.connect(self.deleteApp)
        self.apps[container.id] = widget.ui
        self.groups[container.group.id].app_list_layout.addWidget(widget.ui)

    def show(self):
        self.ui.show()

    # def updateApps(self):
    #     self.apps.clear()
    #     for i in reversed(range(self.ui.app_list_layout.count())):
    #         self.ui.app_list_layout.itemAt(i).widget().setParent(None)
    #     for container in containers_service.getAllContainer():
    #         self.addAppFromContainer(container)

    def moveAppWidget(self, container, widget: AppWidgetUi):
        """
        Reorder the position of App
        @param container: App is being dragged
        @param widget: App is getting dropped
        """
        widget_to_be_moved = self.apps[container.id]

        # Update the in-memory object of container
        update_model_from_dict(widget_to_be_moved.container, model_to_dict(container))
        widget_to_be_moved.parentWidget().layout().removeWidget(widget_to_be_moved)
        index = widget.parentWidget().layout().indexOf(widget)
        widget.parentWidget().layout().insertWidget(index + 1, widget_to_be_moved)

    def moveAppToGroup(self, container, widget: GroupWidgetUi):
        """
        Move an app into a group
        @param container:   Container of the app, which is being dragged
        @param widget: Group which is getting dropped
        """
        widget_to_be_moved = self.apps[container.id]

        # Update the in-memory object of container
        update_model_from_dict(widget_to_be_moved.container, model_to_dict(container))
        widget_to_be_moved.parentWidget().layout().removeWidget(widget_to_be_moved)
        widget.app_list_layout.addWidget(widget_to_be_moved)

    def moveGroup(self, group: Group, widget: GroupWidgetUi):
        """
        Re-order the position of groups
        @param group: Group which is being drag to reorder
        @param widget: Current group
        """
        group_to_be_moved: GroupWidgetUi = self.groups[group.id]
        update_model_from_dict(group_to_be_moved.group, model_to_dict(group))
        group_to_be_moved.parentWidget().layout().removeWidget(group_to_be_moved)
        index = widget.parentWidget().layout().indexOf(widget)
        widget.parentWidget().layout().insertWidget(index + 1, group_to_be_moved)

    def createGroup(self, container, widget: AppWidgetUi):
        """
        Create group when user drag two apps together
        @param container: Container is being dragged
        @param widget: Container is getting dropped
        """
        widget_to_be_moved = self.apps[container.id]
        # Update the in-memory object of container
        update_model_from_dict(widget_to_be_moved.container, model_to_dict(container))
        group = group_service.createGroup(tr('New Group'))
        self.addGroupWidget(group)
        widget_to_be_moved.container.group = group
        widget_to_be_moved.container.save()
        widget.container.group = group
        widget.container.save()
        group_widget = self.groups[group.id]
        self.groups[group.id] = group_widget
        self.ui.app_list.layout().addWidget(group_widget)
        widget_to_be_moved.parentWidget().layout().removeWidget(widget_to_be_moved)
        group_widget.app_list_layout.addWidget(widget_to_be_moved)
        widget.parentWidget().layout().removeWidget(widget)
        group_widget.app_list_layout.addWidget(widget)

    def deleteGroup(self, group: Group, approved=False):
        if not approved:
            message = tr("Are you sure you want to delete this group? All apps inside will be deleted also!")
            button_reply = QMessageBox.question(self.ui, tr('Delete group'), message,
                                                QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
            if button_reply != QMessageBox.Ok:
                return
        for i in reversed(range(self.groups[group.id].app_list_layout.count())):
            container = self.groups[group.id].app_list_layout.itemAt(i).widget().container
            containers_service.deleteContainer(container)
            self.groups[group.id].app_list_layout.itemAt(i).widget().setParent(None)
            del self.apps[container.id]
        self.groups[group.id].deleteLater()
        del self.groups[group.id]
        group_service.deleteGroup(group)

    def deleteApp(self, container):
        message = tr("Are you sure you want to delete this container? All configurations "
                     "you made for it will be deleted also!")
        button_reply = QMessageBox.question(self.ui, tr('Delete container'), message,
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if button_reply != QMessageBox.Ok:
            return
        containers_service.deleteContainer(container)
        self.apps[container.id].deleteLater()
        del self.apps[container.id]

    def onWorkspaceChanged(self, workspace_id: str):
        workspace_service.activeWorkspace(int(workspace_id))
        # Incase we create a new workspace, the new one will not be selected by the time we calling this function
        # So, we pass it as parameter to the search function
        self.search(workspace_id=workspace_id)

    def search(self, data=None, workspace_id=None):
        if workspace_id is None:
            workspace_id = self.ui.workspaces.getCurrentOption()
        workspace = workspace_service.getWorkspaceById(workspace_id)
        keyword = self.ui.search_app.text()

        for group in self.groups:
            self.groups[group].show()

        for app in self.apps:
            self.apps[app].show()

        for app in self.apps:
            if keyword not in self.apps[app].container.name and keyword not in self.apps[app].container.image_name:
                self.apps[app].hide()

        if not workspace.is_default:
            for group in self.groups:
                if self.groups[group].group.workspace.id != workspace.id:
                    self.groups[group].hide()

    def resizeEvent(self, event: QResizeEvent):
        global_preference_service.setHomeWindowSize(event.size())
        QMainWindow.resizeEvent(self.ui, event)

    def showAbout(self):
        about = AboutDialog(None)
        about.show()

    def showPreferences(self):
        preference = GlobalPreferences(None)
        preference.show()

    def onMenuClicked(self):
        menu_help = QMenu(self.ui)
        about = QAction(self.ui)
        about.setMenuRole(QAction.AboutRole)
        about.setText(tr("About"))
        about.triggered.connect(self.showAbout)
        menu_help.addAction(about)
        check_for_update = QAction(self.ui)
        check_for_update.setText(tr("Check for updates"))
        check_for_update.setMenuRole(QAction.ApplicationSpecificRole)
        check_for_update.triggered.connect(lambda: data_transporter_service.fire(UPDATES_CHANNEL, False))
        menu_help.addAction(check_for_update)
        menu_help.addSeparator()

        new_group = QAction(tr("New group…"), self.ui)
        new_group.triggered.connect(lambda: self.addGroupWidget(group_service.createGroup(tr('New Group'))))
        menu_help.addAction(new_group)

        menu_help.addSeparator()

        preferences = QAction(tr("Preferences…"), self.ui)
        preferences.triggered.connect(self.showPreferences)
        menu_help.addAction(preferences)

        menu_help.addSeparator()

        quit_app = QAction(tr("Exit"), self.ui)
        quit_app.triggered.connect(utils.exitApp)
        menu_help.addAction(quit_app)
        point: QPoint = self.ui.mapToGlobal(self.ui.custom_menu.pos())
        point.setY(point.y() + self.ui.custom_menu.height() + rt(5))
        menu_help.exec_(point)
