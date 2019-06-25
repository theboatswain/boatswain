import os

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout

from add.app_widget import AppWidget
from services import docker_service

file_path = __file__
DOCKERHUB_IMG_API = 'https://hub.docker.com/api/content/v1/products/images'


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
        self.dialog.scrollArea.setWidget(self.searchResultArea)
        dialog.keySearch.returnPressed.connect(self.searchApp)

    def searchApp(self):
        keyword = self.dialog.keySearch.text()
        if len(keyword) == 0:
            return
        docker_images = docker_service.search_containers(keyword)
        for item in docker_images:
            # res = requests.get(DOCKERHUB_IMG_API + "/%s" % item['name'])
            # if res.status_code == 200:
            #     avatar_url = res.json()['logo_url']['large']
            #     data = request.urlopen(avatar_url).read()
            #     image = QImage.fromData(data)
            widget = QWidget(self.searchResultArea)
            AppWidget(widget, item['name'], item['description'])
            self.searchResultArea.layout().addWidget(widget)