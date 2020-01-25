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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout, QLabel, QFrame, QLayout

from boatswain.common.models.container import Container
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy, BorderedButton
from boatswain.common.utils.app_avatar import AppAvatar
from boatswain.home.advanced.advanced_app_widget import AdvancedAppWidget


class AppWidgetUi(QWidget):
    """ Class to customise app's widgets """

    def __init__(self, parent, container: Container, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, rt(2), 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setAlignment(Qt.AlignTop)
        self.vertical_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.widget = QWidget(self)
        self.widget.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout.addWidget(self.widget)
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(rt(20), rt(1), rt(10), rt(3))
        self.pic = AppAvatar(container.avatar, container.image_name, parent=self.widget, radius=rt(20))
        self.horizontal_layout.addWidget(self.pic)
        self.name = QLabel(self.widget)
        self.name.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.horizontal_layout.addWidget(self.name)

        self.status = BorderedButton(self.widget)
        self.horizontal_layout.addWidget(self.status)

        self.advanced_app = AdvancedAppWidget(self, container)

        self.vertical_layout.addWidget(self.advanced_app.ui)
        self.container = container

        self.line = QFrame(self)
        self.line.setLineWidth(0)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Plain)
        self.vertical_layout.addWidget(self.line)

        self.setProperty('class', 'app-widget')
