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

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy

from boatswain.common.services.system_service import applyFontRatio, rt


class AppAvatar(QWidget):
    """ Class to customise app's avatar """

    def __init__(self, name, radius=25, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setFixedSize(radius * 2, radius * 2)
        self.avatar_layout = QVBoxLayout(self)
        self.avatar_layout.setContentsMargins(0, 0, 0, 0)
        self.avatar_layout.setSpacing(0)
        self.name = QLabel(self)
        self.name.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(applyFontRatio(20))
        self.name.setFont(font)
        self.avatar_layout.addWidget(self.name, Qt.AlignCenter)
        _translate = QCoreApplication.translate
        self.name.setText(_translate("widget", name))
        self.setLayout(self.avatar_layout)
        self.setStyleSheet("border-radius: " + str(radius) + "px; background: rgb(89, 173, 223); color: white")
        self.status = QWidget(self)
        # self.status.setFixedSize(rt(12), rt(12))
        self.status.setStyleSheet('background: rgb(101, 180, 67); border-radius: ' + str(rt(6)))
        self.status.setGeometry(radius * 1.38, radius * 1.38, rt(12), rt(12))
        self.status.hide()

    def updateStatus(self, is_running):
        if is_running:
            self.status.show()
        else:
            self.status.hide()
