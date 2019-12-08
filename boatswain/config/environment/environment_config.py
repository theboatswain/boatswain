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

import os

from PyQt5 import QtCore
from PyQt5.QtCore import QItemSelectionModel, QModelIndex
from PyQt5.QtWidgets import QTableView, QAbstractItemView

from boatswain.common.models.container import Container
from boatswain.common.models.environment import Environment
from boatswain.common.services import environment_service
from boatswain.common.ui.custom_ui import PathInputDelegate
from boatswain.config.environment.environment_config_model import EnvironmentConfigModel
from boatswain.config.environment.environment_config_ui import EnvironmentConfigUi


class EnvironmentConfig:
    _translate = QtCore.QCoreApplication.translate

    template = 'EnvironmentConfig'

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = EnvironmentConfigUi(parent, container)

        table_data = environment_service.getEnvironments(self.container)
        headers = ['name', 'value', 'description']
        self.configureEnvTable(self.ui.user_table, headers, list(table_data), self.container)
        self.ui.user_table.setItemDelegateForColumn(1, PathInputDelegate(self.ui.user_table))

        sys_headers = ['name', 'value']
        self.configureEnvTable(self.ui.sys_env_table, sys_headers, self.getAllSysEnv(), self.container)
        self.ui.sys_env_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.sys_env_table.doubleClicked.connect(self.onDoubleClickItem)

        self.retranslateUi()

        self.ui.new_env.clicked.connect(self.onNewEnvClicked)
        self.ui.delete_env.clicked.connect(self.onDeleteEnvClicked)

    def retranslateUi(self):
        self.ui.user_env_label.setText(self._translate(self.template, "User environment variables:"))
        self.ui.new_env.setText(self._translate(self.template, "Add"))
        self.ui.delete_env.setText(self._translate(self.template, "Delete"))
        self.ui.include_sys_env.setText(
            self._translate(self.template, "System environments (double click to copy)"))

    def onDoubleClickItem(self, index: QModelIndex):
        data = self.ui.sys_env_table.model().array_data[index.row()]
        self.ui.user_table.model().addRecord(data)
        flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        index = self.ui.user_table.model().index(self.ui.user_table.model().rowCount() - 1, 0)
        self.ui.user_table.selectionModel().select(index, flags)
        self.ui.user_table.resizeRowsToContents()

    def onNewEnvClicked(self):
        self.ui.user_table.model().addRecord(
            Environment(name='NEW_ENV', value='env value', description='description', container=self.container))
        flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        index = self.ui.user_table.model().index(self.ui.user_table.model().rowCount() - 1, 0)
        self.ui.user_table.selectionModel().select(index, flags)
        self.ui.user_table.resizeRowsToContents()

    def onDeleteEnvClicked(self):
        indicates = self.ui.user_table.selectionModel().selectedRows()
        for item in sorted(indicates, reverse=True):
            self.ui.user_table.model().removeRow(item.row())
        self.ui.user_table.resizeRowsToContents()

    def getAllSysEnv(self):
        envs = []
        for item in os.environ:
            if item != 'PATH':
                envs.append(Environment(name=item, value=os.environ[item], container=self.container))
        return envs

    def configureEnvTable(self, tv: QTableView, header, data, container: Container):
        # set the table model
        table_model = EnvironmentConfigModel(data, header, container, self.ui)
        tv.setModel(table_model)

        # hide grid
        tv.setShowGrid(False)

        # # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        hh.setMinimumSectionSize(100)

        # set column width to fit contents
        tv.resizeColumnsToContents()

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(True)

        tv.setSelectionBehavior(QAbstractItemView.SelectRows)
        return table_model
