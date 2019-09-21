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

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QLabel, QGridLayout, QPushButton, QComboBox, QLineEdit, QCheckBox, QWidget, QVBoxLayout, \
    QHBoxLayout, QFrame

from boatswain.common.models.container import Container
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy, AutoResizeWidget
from boatswain.common.utils.app_avatar import AppAvatar


class GeneralAppConfigUi(AutoResizeWidget):

    def __init__(self, parent, container: Container, handler) -> None:
        super().__init__(parent)
        self.container = container
        self.handler = handler
        self.vertical_layout_2 = QVBoxLayout(self)
        self.vertical_layout_2.setContentsMargins(rt(20), rt(11), rt(20), rt(11))
        self.vertical_layout_2.setSpacing(rt(6))
        self.widget = QWidget(self)
        self.widget.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.horizontal_layout_2 = QHBoxLayout(self.widget)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(rt(6))

        self._translate = QCoreApplication.translate
        self.pic = AppAvatar(container, parent=self, radius=rt(20))

        self.horizontal_layout_2.addWidget(self.pic)
        self.container_name = QLineEdit(self.widget)

        # Remove the border outline on focus
        self.container_name.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.container_name.setStyleSheet('border: none; background-color: transparent')
        self.container_name.setFocusPolicy(Qt.StrongFocus)
        self.container_name.setFocus()
        self.horizontal_layout_2.addWidget(self.container_name)
        self.widget_5 = QWidget(self.widget)
        self.widget_5.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout_2.addWidget(self.widget_5)
        self.vertical_layout_2.addWidget(self.widget)
        self.line_3 = QFrame(self)
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.vertical_layout_2.addWidget(self.line_3)
        self.widget_3 = QWidget(self)
        self.widget_3.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.vertical_layout_4 = QVBoxLayout(self.widget_3)
        self.vertical_layout_4.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_4.setSpacing(rt(6))
        self.repo_source = QLabel(self.widget_3)
        self.vertical_layout_4.addWidget(self.repo_source)
        self.container_id = QLabel(self.widget_3)
        self.vertical_layout_4.addWidget(self.container_id)
        self.vertical_layout_2.addWidget(self.widget_3)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.vertical_layout_2.addWidget(self.line)
        self.widget_4 = QWidget(self)
        self.widget_4.setSizePolicy(BQSizePolicy(v_stretch=2))
        self.grid_layout = QGridLayout(self.widget_4)
        self.grid_layout.setContentsMargins(0, 0, 0, rt(5))
        self.grid_layout.setSpacing(rt(6))
        self.sync = QPushButton(self.widget_4)
        self.sync.setFocusPolicy(Qt.NoFocus)
        self.grid_layout.addWidget(self.sync, 2, 4, 1, 1)
        self.widget_8 = QWidget(self.widget_4)
        self.widget_8.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.grid_layout.addWidget(self.widget_8, 2, 5, 1, 1)
        self.img_tag_label = QLabel(self.widget_4)
        self.grid_layout.addWidget(self.img_tag_label, 2, 0, 1, 1)
        self.memory_unit = QComboBox(self.widget_4)
        self.grid_layout.addWidget(self.memory_unit, 3, 2, 1, 1)
        self.cpu_unit = QComboBox(self.widget_4)
        self.grid_layout.addWidget(self.cpu_unit, 4, 2, 1, 1)
        self.widget_7 = QWidget(self.widget_4)
        self.widget_7.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.grid_layout.addWidget(self.widget_7, 3, 3, 1, 1)
        self.limit_cpu_label = QLabel(self.widget_4)
        self.grid_layout.addWidget(self.limit_cpu_label, 4, 0, 1, 1)
        self.entrypoint_label = QLabel(self.widget_4)
        self.grid_layout.addWidget(self.entrypoint_label, 5, 0, 1, 1)
        self.image_tags = QComboBox(self.widget_4)
        self.grid_layout.addWidget(self.image_tags, 2, 1, 1, 3)
        self.limit_memory_label = QLabel(self.widget_4)
        self.grid_layout.addWidget(self.limit_memory_label, 3, 0, 1, 1)
        self.limit_memory = QLineEdit(self.widget_4)
        self.limit_memory.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.limit_memory.setFocusPolicy(Qt.ClickFocus)
        self.limit_memory.setText(str(self.container.memory_limit))
        self.limit_memory.setValidator(QIntValidator(0, 9999999))
        self.grid_layout.addWidget(self.limit_memory, 3, 1, 1, 1)
        self.limit_cpu = QLineEdit(self.widget_4)
        self.limit_cpu.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.limit_cpu.setFocusPolicy(Qt.ClickFocus)
        self.limit_cpu.setText(str(self.container.cpu_limit))
        self.limit_cpu.setValidator(QDoubleValidator(0, 99999999, 2))
        self.grid_layout.addWidget(self.limit_cpu, 4, 1, 1, 1)
        self.entrypoint = QLineEdit(self.widget_4)
        self.entrypoint.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.entrypoint.setFocusPolicy(Qt.ClickFocus)
        self.grid_layout.addWidget(self.entrypoint, 5, 1, 1, 3)
        self.vertical_layout_2.addWidget(self.widget_4)
        self.line_2 = QFrame(self)
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.vertical_layout_2.addWidget(self.line_2)
        self.widget_2 = QWidget(self)
        self.widget_2.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.vertical_layout_3 = QVBoxLayout(self.widget_2)
        self.vertical_layout_3.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_3.setSpacing(rt(6))
        self.start_with_boatswain = QCheckBox(self.widget_2)
        self.vertical_layout_3.addWidget(self.start_with_boatswain)
        self.stop_with_boatswain = QCheckBox(self.widget_2)
        self.vertical_layout_3.addWidget(self.stop_with_boatswain)
        self.vertical_layout_2.addWidget(self.widget_2)

        self.container_id.setTextInteractionFlags(Qt.TextSelectableByMouse)
