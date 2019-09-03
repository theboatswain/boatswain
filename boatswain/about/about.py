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

from PyQt5.QtCore import QCoreApplication, QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog

from boatswain.about.about_ui import AboutUi
from boatswain.about.license.license_ui import LicenseUi
from boatswain.resources.acknowledge import acknowledge
from boatswain.resources_utils import get_resource


class AboutDialog(object):

    _translate = QCoreApplication.translate
    template = 'About'

    def __init__(self, parent) -> None:
        super().__init__()
        self.dialog = QDialog(parent)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.ui = AboutUi(self.dialog)
        self.dialog.ui = self.ui
        self.ui.app_image_widget.resizeEvent = self.resizeEvent
        self.ui.acknowledge_widget.setStyleSheet('background: white')
        self.ui.acknowledge.setText(acknowledge)
        self.ui.license.clicked.connect(self.showLicense)

    def show(self):
        self.dialog.exec_()

    def resizeEvent(self, event):
        height = event.size().height() * 0.8
        pixmap = QIcon(get_resource('resources/logo/boatswain.svg')).pixmap(QSize(height, height))
        self.ui.avatar.setPixmap(pixmap)

    def showLicense(self):
        dialog = QDialog(self.dialog)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.ui = LicenseUi(dialog)
        dialog.exec_()
