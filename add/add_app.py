import os

from PyQt5 import uic
from PyQt5.QtCore import Qt

from services import docker_service

file_path = __file__


class AddAppDialog(object):

    def __init__(self, title, dialog) -> None:
        super().__init__()
        self.title = title
        self.dialog = dialog
        ui_dir = os.path.dirname(file_path)
        uic.loadUi(os.path.join(ui_dir, 'add_app.ui'), dialog)
        dialog.setWindowTitle(self.title)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.keySearch.returnPressed.connect(self.searchApp)

    def searchApp(self):
        keyword = self.dialog.keySearch.text()
        if len(keyword) == 0:
            return
        images = docker_service.search_containers(keyword)
        print(images)
