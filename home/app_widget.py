import docker
from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt, QPropertyAnimation, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout, QSizePolicy, QFrame
from docker.errors import ContainerError, ImageNotFound, APIError

from common.models.container import Container
from common.models.environment import Environment
from common.models.port_mapping import PortMapping
from common.utils import text_utils
from common.utils.app_avatar import AppAvatar
from common.utils.custom_ui import BQSizePolicy


class AppWidget(QWidget):
    """ Class to customise app's widgets """
    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 2, 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setAlignment(Qt.AlignTop)
        widget = QWidget(self)
        widget.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout.addWidget(widget)
        self.horizontal_layout = QHBoxLayout(widget)
        self.horizontal_layout.setContentsMargins(20, 2, 10, 5)
        _translate = QCoreApplication.translate

        img_name = container.image_name
        name_part = container.image_name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=widget, radius=21)
        self.horizontal_layout.addWidget(self.pic)
        self.name = QLabel(widget)
        self.name.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.name.setObjectName("name")
        self.horizontal_layout.addWidget(self.name)

        self.start = QPushButton(widget)
        self.start.setObjectName("start")
        self.start.setFlat(True)
        self.start.setStyleSheet("border: 1px solid #999999; padding: 1px 10px; border-radius: 2px")
        self.horizontal_layout.addWidget(self.start)

        self.app_info = QWidget(self)
        self.app_info.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout.addWidget(self.app_info)
        self.container_info = container

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.vertical_layout.addWidget(line)

        # Init for 'start' button
        self.start.setText(_translate("widget", "Start"))
        self.start.setEnabled(True)
        self.name.setText(_translate("widget", container.image_name))

        self.is_app_info_opened = False

        QMetaObject.connectSlotsByName(self)

    @pyqtSlot(bool, name="on_start_clicked")
    def control_app(self, checked):
        docker_client = docker.from_env()
        """ Docker docker_container should have:
            - Image: <url>/<image_name>:<tag> if tag is not provided, get latest
            - Name (unique)
            - Detach mode should be enabled
            - ports
            - environment 
        """
        # TODO having more statuses to be handled
        if self.container_info.status != 'RUNNING':
            self.start_app(docker_client)
        else:
            self.stop_app(docker_client)

    def stop_app(self, client):
        try:
            docker_container = client.containers.get(self.container_info.container_id)
            docker_container.stop(timeout=20)
            self.container_info.status = 'STOPPED'
            self.start.setText('Start')
        except ContainerError:
            print("got ContainerError error")
        except ImageNotFound:
            print('got ImageNotFound error')
        except APIError:
            print('got APIError error')

    def start_app(self, client):
        try:
            if not self.container_info.container_id and self.container_info.container_id != "":
                docker_container = client.containers.get(self.container_info.container_id)
                docker_container.start()
            else:
                container_envs = []
                for environment in Environment.select():
                    if environment.container == self.container_info:
                        container_envs.append(environment.name + '=' + environment.value)

                ports = {}
                for port in PortMapping.select():
                    if port.container == self.container_info:
                        ports[str(port.port) + '/' + port.protocol] = port.targetPort

                docker_container = client.containers.run(
                    self.container_info.image_name + ":" + self.container_info.tag,
                    detach=True, ports=ports, environment=container_envs)
                self.container_info.container_id = docker_container.short_id

            self.container_info.status = 'RUNNING'
            self.container_info.save()
            self.start.setText('Running')
        except ContainerError:
            print("got ContainerError error")
        except ImageNotFound:
            print('got ImageNotFound error')
        except APIError:
            print('got APIError error')

    def mouseReleaseEvent(self, event):
        if not self.is_app_info_opened:
            self.expanding = QPropertyAnimation(self.app_info, b"minimumHeight")
            self.expanding.setDuration(300)
            self.expanding.setStartValue(0)
            self.expanding.setEndValue(150)
            self.expanding.start()
            self.is_app_info_opened = True
        else:
            self.collapsing = QPropertyAnimation(self.app_info, b"minimumHeight")
            self.collapsing.setDuration(300)
            self.collapsing.setStartValue(150)
            self.collapsing.setEndValue(0)
            self.collapsing.start()
            self.is_app_info_opened = False
        QWidget.mouseReleaseEvent(self, event)
