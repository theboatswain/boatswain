import os

from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QLineEdit, QWidget, QSizePolicy, QVBoxLayout

from controllers.add.add_app import AddAppDialog
from controllers.home.app_widget import AppWidget
from domains import base
from domains.container import Container
from services import data_transporter_service
from utils.constants import CONTAINER_CHANNEL, APP_EXIT_CHANNEL

file_path = __file__


class Home(QMainWindow):

    def __init__(self):
        super(Home, self).__init__()
        ui_dir = os.path.dirname(file_path)
        uic.loadUi(os.path.join(ui_dir, 'home.ui'), self)
        self.show()
        data_transporter_service.listen(CONTAINER_CHANNEL, self.addAppFromContainer)

        self.searchResultArea = QWidget(self)
        self.searchResultArea.setObjectName('searchResultArea')
        self.searchResultArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        layout = QVBoxLayout(self.searchResultArea)
        layout.setAlignment(Qt.AlignTop)
        self.searchResultArea.setLayout(layout)
        self.searchResultArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.searchResultArea)

    @pyqtSlot(bool, name='on_addApp_clicked')
    @pyqtSlot(bool, name='on_actionAdd_triggered')
    def addAppClicked(self, checked=None):
        if checked is None:
            return
        dialog = QDialog()
        dialog.ui = AddAppDialog("Add app", dialog)
        dialog.exec_()

    def addAppFromContainer(self, container: Container):
        widget = AppWidget(self.searchResultArea, container)
        self.searchResultArea.layout().addWidget(widget)

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)

    def closeEvent(self, event):
        data_transporter_service.fire(APP_EXIT_CHANNEL, True)
        event.accept()
