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
from PyQt5.QtCore import QSize

from boatswain.common.models.container import Container
from boatswain.common.utils.custom_ui import BQSizePolicy


class PreferencesShortcutConfigUi(object):

    def __init__(self, dialog, container: Container, handler) -> None:
        self.container = container
        self.handler = handler
        self.dialog = dialog
        dialog.resize(745, 314)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(745, 314))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.top_widget = QtWidgets.QWidget(dialog)
        self.top_widget.setSizePolicy(BQSizePolicy())
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.top_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.import_shortcut = QtWidgets.QPushButton(self.top_widget)
        self.horizontalLayout.addWidget(self.import_shortcut)
        self.export_shortcut = QtWidgets.QPushButton(self.top_widget)
        self.horizontalLayout.addWidget(self.export_shortcut)
        self.hidden = QtWidgets.QWidget(self.top_widget)
        self.hidden.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontalLayout.addWidget(self.hidden)
        self.new_shortcut = QtWidgets.QPushButton(self.top_widget)
        self.horizontalLayout.addWidget(self.new_shortcut)
        self.delete_shortcut = QtWidgets.QPushButton(self.top_widget)
        self.horizontalLayout.addWidget(self.delete_shortcut)
        self.verticalLayout.addWidget(self.top_widget)
        self.shortcut_table = QtWidgets.QTableView(dialog)
        self.verticalLayout.addWidget(self.shortcut_table)
