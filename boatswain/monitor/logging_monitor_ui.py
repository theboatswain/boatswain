from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QObject, Qt
from PyQt5.QtWidgets import QDialog, QStyle, QTableView

from boatswain.common.models.container import Container
from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.ui.custom_ui import BQSizePolicy


class LoggingMonitorUi(QObject):
    def __init__(self, dialog: QDialog, container: Container) -> None:
        super().__init__()
        height = system_service.screen_height / 2
        width = height * 2
        dialog.resize(width, height)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(width, height))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.top_widget = QtWidgets.QWidget(dialog)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.top_widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.tool_widget = QtWidgets.QWidget(self.top_widget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tool_widget)
        self.horizontalLayout.setContentsMargins(rt(12), rt(6), rt(12), rt(6))
        self.horizontalLayout.setSpacing(rt(6))
        self.now = QtWidgets.QPushButton(self.tool_widget)
        self.now.setCheckable(True)
        self.now.setChecked(True)
        self.now.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.now)
        self.hidden_1 = QtWidgets.QWidget(self.tool_widget)
        self.hidden_1.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontalLayout.addWidget(self.hidden_1)
        self.clear = QtWidgets.QPushButton(self.tool_widget)
        self.clear.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.clear)
        self.reload = QtWidgets.QPushButton(self.tool_widget)
        self.reload.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.reload)
        self.hidden_2 = QtWidgets.QWidget(self.tool_widget)
        self.hidden_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontalLayout.addWidget(self.hidden_2)
        self.info = QtWidgets.QPushButton(self.tool_widget)
        self.info.setFocusPolicy(Qt.NoFocus)
        self.horizontalLayout.addWidget(self.info)
        self.hidden = QtWidgets.QWidget(self.tool_widget)
        self.horizontalLayout.addWidget(self.hidden)
        self.search = QtWidgets.QLineEdit(self.tool_widget)
        self.search.setSizePolicy(BQSizePolicy(h_stretch=3))
        self.horizontalLayout.addWidget(self.search)
        self.verticalLayout_2.addWidget(self.tool_widget)
        self.verticalLayout.addWidget(self.top_widget)
        self.log_widget = QtWidgets.QWidget(dialog)
        self.log_widget.setSizePolicy(BQSizePolicy(v_stretch=3))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.log_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(rt(6))
        self.log_list_table = QTableView(dialog)
        self.verticalLayout_3.addWidget(self.log_list_table)
        self.verticalLayout.addWidget(self.log_widget)

        self.retranslateUi()

    def retranslateUi(self):
        self.now.setText(self.tr("Now"))
        self.clear.setText(self.tr("Clear"))
        self.reload.setText(self.tr("Reload"))
        self.info.setText(self.tr("Info"))
