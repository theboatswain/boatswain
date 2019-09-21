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
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel

from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.common.utils.constants import SEARCH_APP_WIDTH
from boatswain.resources_utils import getResource


class ShortAppWidgetUi(QWidget):

    def __init__(self, parent_widget, ui_handler) -> None:
        super().__init__(parent_widget)
        self.ui_handler = ui_handler
        self.setMinimumSize(QtCore.QSize(rt(SEARCH_APP_WIDTH), rt(136)))
        self.setMaximumHeight(rt(136))
        self.setMaximumWidth(rt(SEARCH_APP_WIDTH))
        self.central_layout = QtWidgets.QVBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_widget = QWidget(self)
        self.central_layout.addWidget(self.central_widget)

        self.horizontal_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(rt(10))
        self.avatar_area = QtWidgets.QWidget(self)

        self.icon = QLabel(self.avatar_area)
        self.icon.setPixmap(QIcon(getResource('resources/icons/docker.svg'))
                            .pixmap(QSize(rt(32), rt(32))))

        self.avatar_area.setStyleSheet('background: rgb(89, 173, 223)')
        self.avatar_layout = QtWidgets.QVBoxLayout(self.avatar_area)
        self.avatar_layout.setContentsMargins(rt(8), rt(5), rt(8), rt(5))
        self.avatar_layout.addWidget(self.icon)
        self.avatar_layout.setAlignment(QtCore.Qt.AlignTop)
        self.horizontal_layout.addWidget(self.avatar_area)
        self.description_area = QtWidgets.QWidget(self)
        self.description_area.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.description_area)
        self.verticalLayout.setContentsMargins(0, 0, 0, rt(6))
        self.verticalLayout.setSpacing(rt(4))
        self.name = QtWidgets.QLabel(self.description_area)
        font = QtGui.QFont()
        font.setPointSize(applyFontRatio(14))
        font.setBold(True)
        font.setWeight(65)
        self.name.setFont(font)
        self.verticalLayout.addWidget(self.name)
        self.description = QtWidgets.QLabel(self.description_area)
        self.description.setSizePolicy(BQSizePolicy(v_stretch=2))
        font = QtGui.QFont()
        font.setPointSize(applyFontRatio(12))
        self.description.setFont(font)
        self.description.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.description.setWordWrap(True)
        self.verticalLayout.addWidget(self.description)
        self.tags_widget = QtWidgets.QWidget(self.description_area)
        self.horizontal_layout_3 = QtWidgets.QHBoxLayout(self.tags_widget)
        self.horizontal_layout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontal_layout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_3.setSpacing(rt(6))
        self.is_official = QtWidgets.QLabel(self.tags_widget)
        self.is_official.setFont(font)
        self.horizontal_layout_3.addWidget(self.is_official)
        self.from_repo = QtWidgets.QLabel(self.tags_widget)
        self.from_repo.setFont(font)
        self.horizontal_layout_3.addWidget(self.from_repo)
        self.verticalLayout.addWidget(self.tags_widget)
        self.line = QtWidgets.QFrame(self.description_area)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.widget = QtWidgets.QWidget(self.description_area)
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(rt(6))
        self.addition_widget = QtWidgets.QWidget(self.widget)
        self.addition_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout_4 = QtWidgets.QHBoxLayout(self.addition_widget)
        self.horizontal_layout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_4.setSpacing(rt(6))
        self.stars = QtWidgets.QLabel(self.addition_widget)
        self.horizontal_layout_4.addWidget(self.stars)
        self.horizontal_layout_2.addWidget(self.addition_widget)
        self.install = QtWidgets.QPushButton(self.widget)
        self.install.setFlat(True)
        self.install.setStyleSheet('border: 1px solid green; padding: 1px 6px')
        self.horizontal_layout_2.addWidget(self.install)
        self.verticalLayout.addWidget(self.widget)
        self.horizontal_layout.addWidget(self.description_area)

        self.end_line = QtWidgets.QFrame(self)
        self.end_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.end_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.central_layout.addWidget(self.end_line)
