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
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableView, QCheckBox

from boatswain.common.models.container import Container
from boatswain.common.services import system_service
from boatswain.common.utils.custom_ui import BQSizePolicy, AutoResizeWidget


class EnvironmentConfigUi(AutoResizeWidget):

    def __init__(self, parent_widget, container: Container) -> None:
        super().__init__(parent_widget)
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
        self.horizontal_layout.addWidget(self.new_env)
        self.delete_env = QPushButton(self.top_widget)
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
        self.horizontal_layout_2.addWidget(self.include_sys_env)
        self.vertical_layout.addWidget(self.include_sys_env)
        self.sys_env_table = QTableView(self)
        self.vertical_layout.addWidget(self.sys_env_table)

    def preferableSize(self) -> QSize:
        size = super().preferableSize()
        return QSize(size.width(), size.height() * 1.2)
