import os

from PyQt5 import QtCore
from PyQt5.QtCore import QSize, pyqtSlot, QItemSelectionModel, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableView, QCheckBox, \
    QAbstractItemView

from common.models.container import Container
from common.models.environment import Environment
from common.services import config_service
from common.utils.constants import INCLUDING_ENV_SYSTEM
from common.utils.custom_ui import BQSizePolicy, AutoResizeWidget
from config.models.user_env_model import UserEnvModel


class EnvironmentVariable(AutoResizeWidget):
    def preferableSize(self) -> QSize:
        return QSize(705, 555)

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(11, 11, 11, 11)
        self.vertical_layout.setSpacing(6)
        self.top_widget = QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy())
        self.horizontal_layout = QHBoxLayout(self.top_widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(6)
        self.user_env_label = QLabel(self.top_widget)
        self.horizontal_layout.addWidget(self.user_env_label)
        self.hidden_widget = QWidget(self.top_widget)
        self.hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.hidden_widget)
        self.new_env = QPushButton(self.top_widget)
        self.new_env.setObjectName("newEnv")
        self.horizontal_layout.addWidget(self.new_env)
        self.delete_env = QPushButton(self.top_widget)
        self.delete_env.setObjectName("deleteEnv")
        self.horizontal_layout.addWidget(self.delete_env)
        self.vertical_layout.addWidget(self.top_widget)
        self.user_table = QTableView(self)
        self.user_table.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.vertical_layout.addWidget(self.user_table)
        self.mid_widget = QWidget(self)
        self.mid_widget.setSizePolicy(BQSizePolicy())
        self.horizontal_layout_2 = QHBoxLayout(self.mid_widget)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(6)
        self.include_sys_env = QCheckBox(self.mid_widget)
        self.include_sys_env.setObjectName("includeSysEnv")
        self.horizontal_layout_2.addWidget(self.include_sys_env)
        self.vertical_layout.addWidget(self.include_sys_env)
        self.sys_env_table = QTableView(self)
        self.vertical_layout.addWidget(self.sys_env_table)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        table_data = Environment.select().where(Environment.container == self.container)
        headers = ['name', 'value', 'description']
        self.configureUserTable(self.user_table, headers, list(table_data))
        sys_headers = ['name', 'value']
        self.configureUserTable(self.sys_env_table, sys_headers, self.getAllSysEnv())
        self.sys_env_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        if config_service.isAppConf(self.container, INCLUDING_ENV_SYSTEM, 'true'):
            self.include_sys_env.setChecked(True)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.user_env_label.setText(_translate("MainWindow", "User environment variables:"))
        self.new_env.setText(_translate("MainWindow", "New"))
        self.delete_env.setText(_translate("MainWindow", "Delete"))
        self.include_sys_env.setText(_translate("MainWindow", " Include System environment variables (except PATH):"))

    @pyqtSlot(bool, name='on_newEnv_clicked')
    def onNewEnvClicked(self, checked):
        self.user_table.model().addRecord(
            Environment(name='NEW_ENV', value='env value', description='description', container=self.container))
        self.user_table.resizeRowToContents(self.user_table.model().rowCount() - 1)
        flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        index = self.user_table.model().index(self.user_table.model().rowCount() - 1, 0)
        self.user_table.selectionModel().select(index, flags)

    @pyqtSlot(bool, name='on_deleteEnv_clicked')
    def onDeleteEnvClicked(self, checked):
        indicates = self.user_table.selectionModel().selectedRows()
        for item in sorted(indicates):
            self.user_table.model().removeRow(item.row())

    @pyqtSlot(int, name='on_includeSysEnv_stateChanged')
    def onIncludeSysEnvCheck(self, state):
        val = 'true' if state == Qt.Checked else 'false'
        config_service.setAppConf(self.container, INCLUDING_ENV_SYSTEM, val)

    def getAllSysEnv(self):
        envs = []
        for item in os.environ:
            if item != 'PATH':
                envs.append(Environment(name=item, value=os.environ[item]))
        return envs

    def configureUserTable(self, tv: QTableView, header, data):
        # set the table model
        table_model = UserEnvModel(data, header, self)
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
