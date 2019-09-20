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
import requests
from PyQt5.QtCore import Qt, QCoreApplication, QRect, QPoint, QSize
from PyQt5.QtGui import QFont, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy

from boatswain.common.models.container import Container
from boatswain.common.services import containers_service
from boatswain.common.services.system_service import applyFontRatio, rt
from boatswain.common.utils import text_utils


class AppAvatar(QWidget):
    """ Class to customise app's avatar """

    def __init__(self, container: Container, radius=25, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.setFixedSize(radius * 2, radius * 2)
        self.avatar_layout = QVBoxLayout(self)
        self.avatar_layout.setContentsMargins(0, 0, 0, 0)
        self.avatar_layout.setSpacing(0)
        logo_path = container.avatar
        if logo_path:
            self.icon = QLabel(self)
            pixmap = QIcon(logo_path).pixmap(QSize(rt(32), rt(32)))
            self.icon.setPixmap(pixmap)
            self.icon.setAlignment(Qt.AlignCenter)
            self.avatar_layout.addWidget(self.icon, Qt.AlignCenter)
            color = self.analyzeColor(pixmap.toImage())
            color_str = "rgb(%d, %d, %d)" % (color.red(), color.green(), color.blue())
            self.setStyleSheet("border-radius: %dpx; background: %s; color: white" % (radius, color_str))
        else:
            self.name = QLabel(self)
            self.name.setAlignment(Qt.AlignCenter)
            font = QFont()
            font.setPointSize(applyFontRatio(20))
            self.name.setFont(font)
            self.avatar_layout.addWidget(self.name, Qt.AlignCenter)
            _translate = QCoreApplication.translate
            img_name = container.image_name
            name_part = container.image_name.split('/')
            if len(name_part) > 1:
                img_name = name_part[1]
            self.name.setText(_translate("widget", text_utils.getSimpleName(img_name)))
            self.setStyleSheet("border-radius: " + str(radius) + "px; background: rgb(89, 173, 223); color: white")

        self.setLayout(self.avatar_layout)
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

    def analyzeColor(self, img: QImage):
        rect: QRect = img.rect()
        mid_top = QPoint(rect.width() / 2 + rect.x(), rect.y())
        top_color = self.getFirstColor(img, mid_top)
        return top_color.lighter(140)

    def getFirstColor(self, img: QImage, point: QPoint, x=False, unit=1):
        color = img.pixelColor(point)
        while color.alpha() == 0:
            if x:
                point.setX(point.x() + unit)
            else:
                point.setY(point.y() + unit)
            color = img.pixelColor(point)
        return color