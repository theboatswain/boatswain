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
from PyQt5.QtWidgets import QTableView, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QSizePolicy, \
    QLabel, QFrame, QHBoxLayout

from boatswain.common.models.container import Container
from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import AutoResizeWidget, BQSizePolicy, BorderedButton
from boatswain.common.ui.select_ui import SelectUi


class PortMappingConfigUi(AutoResizeWidget):

    def preferableSize(self) -> QSize:
        height = system_service.getRefHeight() / 2
        width = height * 1.6
        return QSize(width, height)

    def __init__(self, parent, container: Container, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.container = container
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(rt(11), rt(11), rt(11), rt(11))
        self.vertical_layout.setSpacing(rt(6))
        self.top_widget = QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy())
        self.grid_layout = QGridLayout(self.top_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, rt(12))
        self.grid_layout.setSpacing(rt(6))
        self.ip_addr = QLineEdit(self.top_widget)
        self.ip_addr.setSizePolicy(BQSizePolicy(h_stretch=1, height=QSizePolicy.Fixed))
        self.ip_addr.setReadOnly(True)
        self.grid_layout.addWidget(self.ip_addr, 2, 1, 1, 1)
        self.ip_addr_label = QLabel(self.top_widget)
        self.grid_layout.addWidget(self.ip_addr_label, 2, 0, 1, 1)
        self.network_label = QLabel(self.top_widget)
        self.grid_layout.addWidget(self.network_label, 0, 0, 1, 1)
        self.network = SelectUi(self.top_widget)
        self.grid_layout.addWidget(self.network, 0, 1, 1, 1)
        self.hidden_widget_2 = QWidget(self.top_widget)
        self.hidden_widget_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.grid_layout.addWidget(self.hidden_widget_2, 2, 2, 1, 1)
        self.vertical_layout.addWidget(self.top_widget)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.vertical_layout.addWidget(self.line)
        self.mid_widget = QWidget(self)
        self.mid_widget.setSizePolicy(BQSizePolicy())
        self.horizontal_layout = QHBoxLayout(self.mid_widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(rt(6))
        self.port_label = QLabel(self.mid_widget)
        self.horizontal_layout.addWidget(self.port_label)
        self.hidden_widget = QWidget(self.mid_widget)
        self.hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.hidden_widget)
        self.new_port = BorderedButton(self.mid_widget)
        self.horizontal_layout.addWidget(self.new_port)
        self.delete_port = BorderedButton(self.mid_widget)
        self.horizontal_layout.addWidget(self.delete_port)
        self.vertical_layout.addWidget(self.mid_widget)
        self.mapping_table = QTableView(self)
        self.vertical_layout.addWidget(self.mapping_table)
