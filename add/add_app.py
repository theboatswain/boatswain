import os

from PyQt5 import uic
from PyQt5.QtCore import Qt

file_path = __file__


class AddAppDialog(object):
    def __init__(self, title) -> None:
        super().__init__()
        self.title = title

    def setupUi(self, dialog):
        ui_dir = os.path.dirname(file_path)
        uic.loadUi(os.path.join(ui_dir, 'add_app.ui'), dialog)
        dialog.setWindowTitle(self.title)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
