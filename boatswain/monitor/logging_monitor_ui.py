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

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, QObject, Qt
from PyQt5.QtWidgets import QDialog, QTableView

from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy


class LoggingMonitorUi(QObject):
    def __init__(self, dialog: QDialog) -> None:
        super().__init__()
        height = system_service.screen_height / 2
        width = height * 2
        dialog.resize(width, height)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(width, height))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        self.vertical_layout = QtWidgets.QVBoxLayout(dialog)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)
        self.top_widget = QtWidgets.QWidget(dialog)
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.top_widget)
        self.vertical_layout_2.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_2.setSpacing(0)
        self.tool_widget = QtWidgets.QWidget(self.top_widget)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.tool_widget)
        self.horizontal_layout.setContentsMargins(rt(12), rt(6), rt(12), rt(6))
        self.horizontal_layout.setSpacing(rt(6))
        self.now = QtWidgets.QPushButton(self.tool_widget)
        self.now.setCheckable(True)
        self.now.setChecked(True)
        self.now.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.now)
        self.hidden_1 = QtWidgets.QWidget(self.tool_widget)
        self.hidden_1.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.hidden_1)
        self.clear = QtWidgets.QPushButton(self.tool_widget)
        self.clear.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.clear)
        self.reload = QtWidgets.QPushButton(self.tool_widget)
        self.reload.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.reload)
        self.hidden_2 = QtWidgets.QWidget(self.tool_widget)
        self.hidden_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.hidden_2)
        self.info = QtWidgets.QPushButton(self.tool_widget)
        self.info.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.info)
        self.hidden = QtWidgets.QWidget(self.tool_widget)
        self.horizontal_layout.addWidget(self.hidden)
        self.search = QtWidgets.QLineEdit(self.tool_widget)
        self.search.setSizePolicy(BQSizePolicy(h_stretch=3))
        self.horizontal_layout.addWidget(self.search)
        self.vertical_layout_2.addWidget(self.tool_widget)
        self.vertical_layout.addWidget(self.top_widget)
        self.log_widget = QtWidgets.QWidget(dialog)
        self.log_widget.setSizePolicy(BQSizePolicy(v_stretch=3))
        self.vertical_layout_3 = QtWidgets.QVBoxLayout(self.log_widget)
        self.vertical_layout_3.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_3.setSpacing(rt(6))
        self.log_list_table = QTableView(dialog)
        self.vertical_layout_3.addWidget(self.log_list_table)
        self.vertical_layout.addWidget(self.log_widget)

        self.retranslateUi()

    def retranslateUi(self):
        self.now.setText(self.tr("Now"))
        self.clear.setText(self.tr("Clear"))
        self.reload.setText(self.tr("Reload"))
        self.info.setText(self.tr("Info"))
