import json
import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout

from add.app_widget import AppWidget
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
        self.searchResultArea = QWidget(dialog)
        self.searchResultArea.setObjectName('searchResultArea')
        self.searchResultArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.searchResultArea.setLayout(QVBoxLayout(self.searchResultArea))
        self.searchResultArea.setContentsMargins(0, 0, 0, 0)
        self.dialog.scrollArea.setWidget(self.searchResultArea)
        dialog.keySearch.returnPressed.connect(self.searchApp)

        with open('resources/default_search.json', 'r') as f:
            self.loadResult(json.load(f))

    def searchApp(self):
        keyword = self.dialog.keySearch.text()
        if len(keyword) == 0:
            return
        docker_images = docker_service.search_containers(keyword)
        self.loadResult(docker_images)

    def loadResult(self, docker_images):
        self.cleanSearchResults()
        for item in docker_images:
            widget = AppWidget(self.searchResultArea, item['name'], item['description'])
            self.searchResultArea.layout().addWidget(widget)

    def cleanSearchResults(self):
        while self.searchResultArea.layout().count():
            item = self.searchResultArea.layout().takeAt(0)
            item.widget().deleteLater()