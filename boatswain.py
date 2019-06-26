import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from controllers.home.home import Home

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon()
    app_icon.addFile('resources/icon/boatswain-16x16.png', QSize(16, 16))
    app_icon.addFile('resources/icon/boatswain-24x24.png', QSize(24, 24))
    app_icon.addFile('resources/icon/boatswain-32x32.png', QSize(32, 32))
    app_icon.addFile('resources/icon/boatswain-48x48.png', QSize(48, 48))
    app_icon.addFile('resources/icon/boatswain-256x256.png', QSize(256, 256))
    app.setWindowIcon(app_icon)
    window = Home()
    sys.exit(app.exec_())
