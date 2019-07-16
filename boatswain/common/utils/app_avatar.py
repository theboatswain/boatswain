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

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy


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
        font.setPointSize(20)
        self.name.setFont(font)
        self.avatar_layout.addWidget(self.name, Qt.AlignCenter)
        _translate = QCoreApplication.translate
        self.name.setText(_translate("widget", name))
        self.setLayout(self.avatar_layout)
        self.setStyleSheet("border-radius: " + str(radius) + "px; background: rgb(89, 173, 223); color: white")
