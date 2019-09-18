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

from boatswain.common.services.system_service import rt
from boatswain.common.utils.constants import SEARCH_APP_WIDTH
from boatswain.resources_utils import get_resource


class ShortAppWidgetUi(QWidget):

    def __init__(self, parent_widget, ui_handler) -> None:
        super().__init__(parent_widget)
        self.ui_handler = ui_handler
        self.setMinimumSize(QtCore.QSize(SEARCH_APP_WIDTH, 136))
        self.setMaximumHeight(136)
        self.setMaximumWidth(SEARCH_APP_WIDTH)
        self.central_layout = QtWidgets.QVBoxLayout(self)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_widget = QWidget(self)
        self.central_layout.addWidget(self.central_widget)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.central_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.avatar_area = QtWidgets.QWidget(self)

        self.icon = QLabel(self.avatar_area)
        self.icon.setPixmap(QIcon(get_resource('resources/icons/docker.svg'))
                            .pixmap(QSize(rt(32), rt(32))))

        self.avatar_area.setStyleSheet('background: rgb(89, 173, 223)')
        self.avatar_layout = QtWidgets.QVBoxLayout(self.avatar_area)
        self.avatar_layout.setContentsMargins(8, 5, 8, 5)
        self.avatar_layout.addWidget(self.icon)
        self.avatar_layout.setAlignment(QtCore.Qt.AlignTop)
        self.horizontalLayout.addWidget(self.avatar_area)
        self.description_area = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description_area.sizePolicy().hasHeightForWidth())
        self.description_area.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.description_area)
        self.verticalLayout.setContentsMargins(0, 0, 0, 6)
        self.verticalLayout.setSpacing(4)
        self.name = QtWidgets.QLabel(self.description_area)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(65)
        self.name.setFont(font)
        self.verticalLayout.addWidget(self.name)
        self.description = QtWidgets.QLabel(self.description_area)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.description.setFont(font)
        self.description.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.description.setWordWrap(True)
        self.verticalLayout.addWidget(self.description)
        self.tags_widget = QtWidgets.QWidget(self.description_area)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tags_widget)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(6)
        self.is_official = QtWidgets.QLabel(self.tags_widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.is_official.setFont(font)
        self.horizontalLayout_3.addWidget(self.is_official)
        self.from_repo = QtWidgets.QLabel(self.tags_widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.from_repo.setFont(font)
        self.horizontalLayout_3.addWidget(self.from_repo)
        self.verticalLayout.addWidget(self.tags_widget)
        self.line = QtWidgets.QFrame(self.description_area)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)
        self.widget = QtWidgets.QWidget(self.description_area)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(6)
        self.addition_widget = QtWidgets.QWidget(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addition_widget.sizePolicy().hasHeightForWidth())
        self.addition_widget.setSizePolicy(sizePolicy)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.addition_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(6)
        self.stars = QtWidgets.QLabel(self.addition_widget)
        self.horizontalLayout_4.addWidget(self.stars)
        self.horizontalLayout_2.addWidget(self.addition_widget)
        self.install = QtWidgets.QPushButton(self.widget)
        self.install.setFlat(True)
        self.install.setStyleSheet('border: 1px solid green; padding: 1px 6px')
        self.horizontalLayout_2.addWidget(self.install)
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout.addWidget(self.description_area)

        self.end_line = QtWidgets.QFrame(self)
        self.end_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.end_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.central_layout.addWidget(self.end_line)
