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
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout

from boatswain.common.services.system_service import rt
from boatswain.common.utils import text_utils
from boatswain.common.utils.app_avatar import AppAvatar
from boatswain.common.ui.custom_ui import BQSizePolicy


class ShortAppWidgetUi(QWidget):

    def __init__(self, parent_widget, name, description, ui_handler) -> None:
        super().__init__(parent_widget)
        self.ui_handler = ui_handler
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self._translate = QCoreApplication.translate

        img_name = name
        name_part = name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=self, radius=rt(25))
        self.horizontal_layout.addWidget(self.pic)

        self.info_widget = QWidget(self)
        self.info_layout = QVBoxLayout(self.info_widget)
        self.info_layout.setContentsMargins(rt(5), 0, 0, 0)

        self.name = QLabel(self)
        self.info_layout.addWidget(self.name)

        if len(description) > 0:
            self.description = QLabel(self)
            self.description.setWordWrap(True)
            self.info_layout.addWidget(self.description)
        self.info_widget.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.horizontal_layout.addWidget(self.info_widget)
        self.from_repo = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(60)
        self.from_repo.setFont(font)
        self.horizontal_layout.addWidget(self.from_repo)
        self.install = QPushButton(self)
        self.install.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.install)
