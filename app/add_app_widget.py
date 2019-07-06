import yaml
from PyQt5.QtCore import QMetaObject, QCoreApplication, pyqtSlot, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout

from common.models.environment import Environment
from common.models.port_mapping import PortMapping
from common.services import containers_service, data_transporter_service
from common.services.worker_service import Worker, threadpool
from common.utils import text_utils
from common.utils.app_avatar import AppAvatar
from common.utils.constants import CONTAINER_CHANNEL
from common.utils.custom_ui import BQSizePolicy


class AddAppWidget(QWidget):

    def __init__(self, parent, name, description, supported_app) -> None:
        super().__init__(parent)
        # set supported app list
        self.supported_app = supported_app

        self.disable_button = False
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self._translate = QCoreApplication.translate

        img_name = name
        name_part = name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=self)
        self.horizontal_layout.addWidget(self.pic)

        self.info_widget = QWidget(self)
        self.info_layout = QVBoxLayout(self.info_widget)
        self.info_layout.setContentsMargins(5, 0, 0, 0)

        self.name = QLabel(self)
        self.info_layout.addWidget(self.name)

        if len(description) > 0:
            self.description = QLabel(self)
            self.description.setWordWrap(True)
            self.description.setText(self._translate("widget", description))
            self.info_layout.addWidget(self.description)
        self.info_widget.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.horizontal_layout.addWidget(self.info_widget)
        self.from_repo = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.from_repo.setFont(font)
        self.horizontal_layout.addWidget(self.from_repo)
        self.install = QPushButton(self)
        self.install.setObjectName("install")
        self.install.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.install)
        self.from_repo.setText(self._translate("widget", "From Dockerhub"))
        self.install.setText(self._translate("widget", "Install"))
        self.name.setText(self._translate("widget", name))
        QMetaObject.connectSlotsByName(self)

        if containers_service.is_app_installed(name):
            self.install.setText(self._translate("widget", "Installed"))
            self.disable_button = True

    @pyqtSlot(bool, name='on_install_clicked')
    def install_app(self, checked):
        if self.disable_button:
            return
        self.disable_button = True
        self.install.setText(self._translate("widget", "Installing"))

        # Case of a supported app
        if self.name.text() in self.supported_app:
            app = self.supported_app[self.name.text()]
            environments = []
            for env in app['env']:
                environments.append(Environment(name=env['name'], value=env['value']))
            ports = []
            for port in app['ports']:
                ports.append(PortMapping(port=port['port'], protocol=port['protocol'], targetPort=port['targetPort']))
            worker = Worker(containers_service.install_container, app['image'], 'dockerhub',
                            self.description.text(), app['tag'], environments, ports)
        # Un-supported app
        else:
            worker = Worker(containers_service.install_container, self.name.text(), 'dockerhub',
                            self.description.text(), "latest")
        worker.signals.result.connect(self.on_app_installed)
        threadpool.start(worker)

    def on_app_installed(self, container):
        data_transporter_service.fire(CONTAINER_CHANNEL, container)
        self.install.setText(self._translate("widget", "Installed"))
