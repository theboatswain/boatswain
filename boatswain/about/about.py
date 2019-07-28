from PyQt5.QtCore import QCoreApplication, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog

from boatswain.about.about_ui import AboutUi
from boatswain.about.license.license_ui import LicenseUi
from boatswain.resources.acknowledge import acknowledge


class AboutDialog(object):

    _translate = QCoreApplication.translate
    template = 'About'

    def __init__(self, parent) -> None:
        super().__init__()
        self.dialog = QDialog(parent)
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
        self.ui.avatar.setPixmap(QPixmap(':/logo/boatswain.png').scaled(QSize(height, height), Qt.KeepAspectRatio))

    def showLicense(self):
        dialog = QDialog(self.dialog)
        dialog.ui = LicenseUi(dialog)
        dialog.exec_()