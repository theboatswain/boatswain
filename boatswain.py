import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QDialog

from controllers.add.add_app import AddAppDialog


class Boatswain(QMainWindow):

    def __init__(self):
        super(Boatswain, self).__init__()
        uic.loadUi('boatswain.ui', self)
        self.show()

    @pyqtSlot(bool, name='on_addApp_clicked')
    @pyqtSlot(bool, name='on_actionAdd_triggered')
    def addAppClicked(self, checked=None):
        if checked is None:
            return
        dialog = QDialog()
        dialog.ui = AddAppDialog("Add app", dialog)
        dialog.exec_()

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_icon = QIcon()
    app_icon.addFile('resources/icon/boatswain-16x16.png', QSize(16, 16))
    app_icon.addFile('resources/icon/boatswain-24x24.png', QSize(24, 24))
    app_icon.addFile('resources/icon/boatswain-32x32.png', QSize(32, 32))
    app_icon.addFile('resources/icon/boatswain-48x48.png', QSize(48, 48))
    app_icon.addFile('resources/icon/boatswain-256x256.png', QSize(256, 256))
    app.setWindowIcon(app_icon)
    window = Boatswain()
    sys.exit(app.exec_())
