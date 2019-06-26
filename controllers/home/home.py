import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QLineEdit

from controllers.add.add_app import AddAppDialog
file_path = __file__


class Home(QMainWindow):

    def __init__(self):
        super(Home, self).__init__()
        ui_dir = os.path.dirname(file_path)
        uic.loadUi(os.path.join(ui_dir, 'home.ui'), self)
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