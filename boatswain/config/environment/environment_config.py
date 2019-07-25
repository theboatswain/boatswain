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

import os

from PyQt5 import QtCore
from PyQt5.QtCore import QItemSelectionModel, Qt
from PyQt5.QtWidgets import QTableView, QAbstractItemView

from boatswain.common.models.container import Container
from boatswain.common.models.environment import Environment
from boatswain.common.services import config_service
from boatswain.common.utils.constants import INCLUDING_ENV_SYSTEM
from boatswain.common.utils.custom_ui import PathInputDelegate
from boatswain.config.environment.environment_config_model import EnvironmentConfigModel
from boatswain.config.environment.environment_config_ui import EnvironmentConfigUi


class EnvironmentConfig:
    _translate = QtCore.QCoreApplication.translate

    template = 'EnvironmentConfig'

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = EnvironmentConfigUi(parent, container)

        table_data = Environment.select().where(Environment.container == self.container)
        headers = ['name', 'value', 'description']
        self.configureEnvTable(self.ui.user_table, headers, list(table_data), self.container)
        self.ui.user_table.setItemDelegateForColumn(1, PathInputDelegate(self.ui.user_table))

        sys_headers = ['name', 'value']
        self.configureEnvTable(self.ui.sys_env_table, sys_headers, self.getAllSysEnv(), self.container)
        self.ui.sys_env_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        if config_service.isAppConf(self.container, INCLUDING_ENV_SYSTEM, 'true'):
            self.ui.include_sys_env.setChecked(True)

        self.retranslateUi()

        self.ui.new_env.clicked.connect(self.onNewEnvClicked)
        self.ui.delete_env.clicked.connect(self.onDeleteEnvClicked)
        self.ui.include_sys_env.stateChanged.connect(self.onIncludeSysEnvCheck)

    def retranslateUi(self):
        self.ui.user_env_label.setText(self._translate(self.template, "User environment variables:"))
        self.ui.new_env.setText(self._translate(self.template, "Add"))
        self.ui.delete_env.setText(self._translate(self.template, "Delete"))
        self.ui.include_sys_env.setText(
            self._translate(self.template, " Include System environment variables (except PATH):"))

    def onNewEnvClicked(self):
        self.ui.user_table.model().addRecord(
            Environment(name='NEW_ENV', value='env value', description='description', container=self.container))
        self.ui.user_table.resizeRowToContents(self.ui.user_table.model().rowCount() - 1)
        flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        index = self.ui.user_table.model().index(self.ui.user_table.model().rowCount() - 1, 0)
        self.ui.user_table.selectionModel().select(index, flags)
        self.ui.user_table.resizeRowsToContents()

    def onDeleteEnvClicked(self):
        indicates = self.ui.user_table.selectionModel().selectedRows()
        for item in sorted(indicates, reverse=True):
            self.ui.user_table.model().removeRow(item.row())
        self.ui.user_table.resizeRowsToContents()

    def onIncludeSysEnvCheck(self, state):
        val = 'true' if state == Qt.Checked else 'false'
        config_service.setAppConf(self.container, INCLUDING_ENV_SYSTEM, val)

    def getAllSysEnv(self):
        envs = []
        for item in os.environ:
            if item != 'PATH':
                envs.append(Environment(name=item, value=os.environ[item]))
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
