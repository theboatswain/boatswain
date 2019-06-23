import sys

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QDialog

from add.add_app import AddAppDialog


class Boatswain(QMainWindow):
    def __init__(self):
        super(Boatswain, self).__init__()
        uic.loadUi('boatswain.ui', self)

        self.show()

    @pyqtSlot(bool, name='on_addApp_clicked')
    def addAppClicked(self, checked=None):
        if checked is None:
            return
        dialog = QDialog()
        dialog.ui = AddAppDialog("Add app")
        dialog.ui.setupUi(dialog)
        dialog.exec_()

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Boatswain()
    sys.exit(app.exec_())
