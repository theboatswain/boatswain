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
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QAbstractItemView, QTableView, QInputDialog, QMessageBox

from boatswain.common.exceptions.workspace import WorkspaceAlreadyExistsException
from boatswain.common.services import workspace_service, containers_service, data_transporter_service, group_service
from boatswain.common.services.system_service import rt
from boatswain.common.utils import message_utils
from boatswain.common.utils.constants import WORKSPACE_CHANGED_CHANNEL, DELETE_GROUP_CHANNEL, PERFORMING_SEARCH_CHANNEL
from boatswain.common.utils.utils import tr
from boatswain.preferences.workspace.workspace_preferences_model import WorkspacePreferencesModel
from boatswain.preferences.workspace.workspace_preferences_ui import WorkspacePreferencesUi


class WorkspacePreferences:
    table_model: WorkspacePreferencesModel

    def __init__(self, parent) -> None:
        self.ui = WorkspacePreferencesUi(parent, self)
        self.retranslateUi()

        self.ui.new_workspace.clicked.connect(self.onNewWorkspaceClicked)
        self.ui.delete_workspace.clicked.connect(self.onDeleteWorkspaceClicked)
        self.ui.workspace_table.doubleClicked.connect(self.onDoubleClickItem)
        table_data = self.collectData()
        self.headers = ['id', 'name', 'n_groups', 'n_containers']
        display_headers = [tr('ID'), tr('Name'), tr('Number of groups'), tr('Number of containers')]
        self.configureWorkspaceTable(self.ui.workspace_table, self.headers, display_headers, table_data)

    def collectData(self):
        workspaces = {}
        containers = containers_service.getAllContainer()
        for workspace in workspace_service.getWorkspaces():
            if workspace not in workspaces:
                workspaces[workspace.id] = {'group': {}, 'id': workspace.id, 'name': workspace.name,
                                            'n_groups': 0, 'n_containers': 0}
        groups = group_service.getGroups()
        for group in groups:
            if group.workspace.is_default:
                continue
            if group.id not in workspaces[group.workspace.id]['group']:
                workspaces[group.workspace.id]['group'][group.id] = 0
        for container in containers:
            if container.group.workspace.is_default:
                continue
            workspaces[container.group.workspace.id]['group'][container.group.id] += 1
        result = []
        for workspace in workspaces:
            item = workspaces[workspace]
            item['n_groups'] = len(item['group'])
            item['n_containers'] = sum([item['group'][n] for n in item['group']])
            del item['group']
            result.append(item)
        return result

    def onDoubleClickItem(self, index: QModelIndex):
        data = self.table_model.array_data[index.row()]
        dlg = QInputDialog(self.ui)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText(tr("Workspace name:"))
        dlg.setTextValue(data['name'])
        dlg.resize(rt(300), rt(100))
        ok = dlg.exec_()
        name = dlg.textValue()
        if ok:
            if not workspace_service.isWorkspaceNameAvailable(name):
                message_utils.error(tr('Workspace already exists'),
                                    tr('Please choose a different name for your workspace'))
                return
            workspace = workspace_service.getWorkspaceById(data['id'])
            workspace.name = name
            workspace.save()
            data_transporter_service.fire(WORKSPACE_CHANGED_CHANNEL)
            data['name'] = name
            self.table_model.refresh()

    def retranslateUi(self):
        self.ui.workspace_label.setText(tr("Workspaces:"))
        self.ui.new_workspace.setText(tr("Add"))
        self.ui.delete_workspace.setText(tr("Delete"))

    def onNewWorkspaceClicked(self):
        dlg = QInputDialog(self.ui)
        dlg.setInputMode(QInputDialog.TextInput)
        dlg.setLabelText(tr("Workspace name:"))
        dlg.resize(rt(300), rt(100))
        ok = dlg.exec_()
        name = dlg.textValue()
        if ok:
            try:
                workspace = workspace_service.createWorkspace(name)
                data_transporter_service.fire(WORKSPACE_CHANGED_CHANNEL)
                record = {'group': {}, 'id': workspace.id, 'name': workspace.name, 'n_groups': 0, 'n_containers': 0}
                self.table_model.addRecord(record)
            except WorkspaceAlreadyExistsException:
                message_utils.error(tr('Workspace already exists'),
                                    tr('Please choose a different name for your workspace'))

    def onDeleteWorkspaceClicked(self):
        message = tr("Are you sure you want to delete this workspace? All groups and containers that belongs to it "
                     "will be deleted also!")
        button_reply = QMessageBox.question(self.ui, tr('Delete workspace'), message,
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if button_reply != QMessageBox.Ok:
            return
        indicates = self.ui.workspace_table.selectionModel().selectedRows()
        for item in sorted(indicates, reverse=True):
            record = self.table_model.array_data[item.row()]
            workspace = workspace_service.getWorkspaceById(record['id'])
            # Removing all groups / containers that belongs to this workspace
            groups = group_service.getGroupsFromWorkspace(workspace)
            for group in groups:
                data_transporter_service.fire(DELETE_GROUP_CHANNEL, group, approved=True)
            workspace_service.deleteWorkspace(record['id'])
            # Reloading list of workspaces in main UI
            data_transporter_service.fire(WORKSPACE_CHANGED_CHANNEL)
            # Reloading list of containers in main UI
            data_transporter_service.fire(PERFORMING_SEARCH_CHANNEL)
            self.ui.workspace_table.model().removeRow(item.row())
        self.ui.workspace_table.resizeRowsToContents()

    def configureWorkspaceTable(self, tv: QTableView, header, display_header, data):
        # set the table model
        self.table_model = WorkspacePreferencesModel(data, header, display_header, self.ui)
        tv.setModel(self.table_model)

        # hide grid
        tv.setShowGrid(False)

        # # set column width to fit contents
        # tv.resizeColumnsToContents()

        # # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        hh.setMinimumSectionSize(100)
        tv.resizeColumnsToContents()

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(True)

        tv.setSelectionBehavior(QAbstractItemView.SelectRows)
