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
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout

from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import AutoResizeWidget, BQSizePolicy
from boatswain.common.ui.select_ui import SelectUi
from boatswain.common.utils.utils import tr


class GeneralPreferencesUi(AutoResizeWidget):

    def preferableSize(self) -> QSize:
        height = system_service.getRefHeight() / 2
        width = height * 1.8
        return QSize(width, height * 0.7)

    def __init__(self, parent, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(rt(20), rt(11), rt(20), rt(11))
        self.vertical_layout.setSpacing(rt(6))

        self.top_widget = QtWidgets.QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.gridLayout = QtWidgets.QGridLayout(self.top_widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(rt(6))
        self.hidden_widget_1 = QtWidgets.QWidget(self.top_widget)
        self.gridLayout.addWidget(self.hidden_widget_1, 0, 2, 1, 1)
        self.terminal = SelectUi(self.top_widget)
        self.gridLayout.addWidget(self.terminal, 0, 1, 1, 1)
        self.terminal_label = QtWidgets.QLabel(self.top_widget)
        self.gridLayout.addWidget(self.terminal_label, 0, 0, 1, 1)
        self.terminal_newtab_label = QtWidgets.QLabel(self.top_widget)
        self.gridLayout.addWidget(self.terminal_newtab_label, 1, 0, 1, 1)
        self.terminal_newtab = QtWidgets.QCheckBox(self.top_widget)
        self.gridLayout.addWidget(self.terminal_newtab, 1, 1, 1, 1)
        self.vertical_layout.addWidget(self.top_widget)
        self.top_line = QtWidgets.QFrame(self)
        self.top_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.top_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_layout.addWidget(self.top_line)

        self.bot_widget = QtWidgets.QWidget(self)
        self.bot_widget.setSizePolicy(BQSizePolicy(v_stretch=2))
        self.gridLayout_3 = QtWidgets.QGridLayout(self.bot_widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.language_label = QtWidgets.QLabel(self.bot_widget)
        self.gridLayout_3.addWidget(self.language_label, 5, 0, 1, 1)
        self.start_when_login = QtWidgets.QCheckBox(self.bot_widget)
        self.gridLayout_3.addWidget(self.start_when_login, 4, 1, 1, 1)
        self.fetch_shortcut_label = QtWidgets.QLabel(self.bot_widget)
        self.gridLayout_3.addWidget(self.fetch_shortcut_label, 3, 0, 1, 1)
        self.check_for_update = QtWidgets.QCheckBox(self.bot_widget)
        self.gridLayout_3.addWidget(self.check_for_update, 2, 1, 1, 1)
        self.language = SelectUi(self.bot_widget)
        self.gridLayout_3.addWidget(self.language, 5, 1, 1, 1)
        self.check_for_updates_label = QtWidgets.QLabel(self.bot_widget)
        self.gridLayout_3.addWidget(self.check_for_updates_label, 2, 0, 1, 1)
        self.fetch_shortcut = QtWidgets.QCheckBox(self.bot_widget)
        self.gridLayout_3.addWidget(self.fetch_shortcut, 3, 1, 1, 1)
        self.start_when_login_label = QtWidgets.QLabel(self.bot_widget)
        self.gridLayout_3.addWidget(self.start_when_login_label, 4, 0, 1, 1)
        self.hidden_wiget = QtWidgets.QWidget(self.bot_widget)
        self.gridLayout_3.addWidget(self.hidden_wiget, 2, 2, 1, 1)
        self.vertical_layout.addWidget(self.bot_widget)

        self.retranslateUi()

    def retranslateUi(self):
        self.terminal_label.setText(tr("Preferable terminal:"))
        self.terminal_newtab_label.setText(tr("Open terminal in a new tab if possible:"))
        self.language_label.setText(tr("Default language:"))
        self.fetch_shortcut_label.setText(tr("Automatic fetch preferences shortcuts:"))
        self.check_for_updates_label.setText(tr("Automatic check for updates:"))
        self.start_when_login_label.setText(tr("Start Boatswain when login:"))
