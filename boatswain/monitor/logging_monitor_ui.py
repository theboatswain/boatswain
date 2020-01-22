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

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QSize, QObject, Qt
from PyQt5.QtWidgets import QDialog

from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy, BorderedButton
from boatswain.common.utils.utils import tr
from boatswain.monitor.logging_table_ui import UniformRowHeights


class LoggingMonitorUi(QObject):
    def __init__(self, dialog: QDialog) -> None:
        super().__init__()
        height = system_service.getRefHeight() / 2
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
        self.now = BorderedButton(self.tool_widget)
        self.now.setCheckable(True)
        self.now.setChecked(True)
        self.now.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.now)
        self.hidden_1 = QtWidgets.QWidget(self.tool_widget)
        self.hidden_1.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.hidden_1)
        self.clear = BorderedButton(self.tool_widget)
        self.clear.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.clear)
        self.reload = BorderedButton(self.tool_widget)
        self.reload.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.reload)
        self.hidden_2 = QtWidgets.QWidget(self.tool_widget)
        self.hidden_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.hidden_2)
        self.info = BorderedButton(self.tool_widget)
        self.info.setFocusPolicy(Qt.NoFocus)
        self.info.setCheckable(True)
        self.info.setChecked(True)
        self.horizontal_layout.addWidget(self.info)
        self.hidden = QtWidgets.QWidget(self.tool_widget)
        self.horizontal_layout.addWidget(self.hidden)
        self.search = QtWidgets.QLineEdit(self.tool_widget)
        self.search.setSizePolicy(BQSizePolicy(h_stretch=3))
        self.search.setStyleSheet("padding: 0 0 0 5;")
        self.horizontal_layout.addWidget(self.search)
        self.vertical_layout_2.addWidget(self.tool_widget)
        self.vertical_layout.addWidget(self.top_widget)
        self.log_widget = QtWidgets.QWidget(dialog)
        self.log_widget.setSizePolicy(BQSizePolicy(v_stretch=3))
        self.vertical_layout_3 = QtWidgets.QVBoxLayout(self.log_widget)
        self.vertical_layout_3.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_3.setSpacing(rt(6))

        self.splitter = QtWidgets.QSplitter(self.log_widget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.log_list_table = UniformRowHeights(self.splitter)
        self.log_details = QtWidgets.QWidget(self.splitter)

        self.log_details_layout = QtWidgets.QVBoxLayout(self.log_details)
        self.log_details_layout.setContentsMargins(rt(8), 0, rt(8), rt(2))

        self.log_details_label = QtWidgets.QTextBrowser(self.log_details)
        self.log_details_label.setSizePolicy(BQSizePolicy(height=QtWidgets.QSizePolicy.Expanding))
        self.log_details_layout.addWidget(self.log_details_label)

        self.splitter.setSizes([rt(300), rt(20)])
        self.vertical_layout_3.addWidget(self.splitter)
        self.vertical_layout.addWidget(self.log_widget)

        self.retranslateUi()

    def retranslateUi(self):
        self.now.setText(tr("Now"))
        self.clear.setText(tr("Clear"))
        self.reload.setText(tr("Reload"))
        self.info.setText(tr("Info"))
