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

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTableView

from boatswain.common.models.container import Container
from boatswain.common.utils.custom_ui import AutoResizeWidget, BQSizePolicy


class VolumeMountConfigUi(AutoResizeWidget):

    def preferableSize(self) -> QSize:
        return QSize(745, 354)

    def __init__(self, parent, container: Container, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.container = container
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.top_widget = QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy())
        self.horizontalLayout = QHBoxLayout(self.top_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.volume_label = QLabel(self.top_widget)
        self.horizontalLayout.addWidget(self.volume_label)
        self.hidden_widget = QWidget(self.top_widget)
        self.hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontalLayout.addWidget(self.hidden_widget)
        self.new_mount = QPushButton(self.top_widget)
        self.new_mount.setObjectName("newMount")
        self.horizontalLayout.addWidget(self.new_mount)
        self.delete_mount = QPushButton(self.top_widget)
        self.delete_mount.setObjectName("deleteMount")
        self.horizontalLayout.addWidget(self.delete_mount)
        self.verticalLayout.addWidget(self.top_widget)
        self.mount_table = QTableView(self)
        self.verticalLayout.addWidget(self.mount_table)
