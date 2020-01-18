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
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel, QPushButton, QTableView

from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import AutoResizeWidget, BQSizePolicy


class WorkspacePreferencesUi(AutoResizeWidget):

    def preferableSize(self) -> QSize:
        size = super().preferableSize()
        return QSize(size.width(), size.height() * 0.8)

    def __init__(self, parent, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(rt(11), rt(11), rt(11), rt(11))
        self.verticalLayout.setSpacing(rt(6))
        self.top_widget = QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy())
        self.horizontalLayout = QHBoxLayout(self.top_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(rt(6))
        self.workspace_label = QLabel(self.top_widget)
        self.horizontalLayout.addWidget(self.workspace_label)
        self.hidden_widget = QWidget(self.top_widget)
        self.hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontalLayout.addWidget(self.hidden_widget)
        self.new_workspace = QPushButton(self.top_widget)
        self.horizontalLayout.addWidget(self.new_workspace)
        self.delete_workspace = QPushButton(self.top_widget)
        self.horizontalLayout.addWidget(self.delete_workspace)
        self.verticalLayout.addWidget(self.top_widget)
        self.workspace_table = QTableView(self)
        self.verticalLayout.addWidget(self.workspace_table)
