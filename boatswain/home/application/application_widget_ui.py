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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLabel, QPushButton, QFrame

from boatswain.common.models.container import Container
from boatswain.common.utils import text_utils
from boatswain.common.utils.app_avatar import AppAvatar
from boatswain.common.utils.custom_ui import BQSizePolicy
from boatswain.home.advanced.advanced_app_widget import AdvancedAppWidget


class AppWidgetUi(QWidget):
    """ Class to customise app's widgets """

    def __init__(self, parent, container: Container, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 2, 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setAlignment(Qt.AlignTop)
        self.widget = QWidget(self)
        self.widget.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout.addWidget(self.widget)
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(20, 2, 10, 5)

        img_name = container.image_name
        name_part = container.image_name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=self.widget, radius=20)
        self.horizontal_layout.addWidget(self.pic)
        self.name = QLabel(self.widget)
        self.name.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.horizontal_layout.addWidget(self.name)

        self.status = QPushButton(self.widget)
        self.status.setFlat(True)
        self.status.setStyleSheet("border: 1px solid #999999; padding: 1px 10px; border-radius: 2px")
        self.horizontal_layout.addWidget(self.status)

        self.advanced_app = AdvancedAppWidget(self.widget, container)

        self.vertical_layout.addWidget(self.advanced_app.ui)
        self.container_info = container

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.vertical_layout.addWidget(line)
