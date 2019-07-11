from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt, QPropertyAnimation, pyqtSlot
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout, QSizePolicy, QFrame

from common.exceptions.docker_exceptions import DockerNotAvailableException
from common.models.container import Container
from common.services import containers_service
from common.services.worker_service import Worker, threadpool
from common.utils import text_utils, docker_utils
from common.utils.app_avatar import AppAvatar
from common.utils.custom_ui import BQSizePolicy
from home.advanced_app_widget import AdvancedAppWidget


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
        widget.mouseReleaseEvent = self.onAppClicked
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

        self.app_info = AdvancedAppWidget(widget, container)
        self.app_info_max_height = self.app_info.sizeHint().height() + 10
        self.app_info.setMaximumHeight(0)

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

        QMetaObject.connectSlotsByName(self)

    @pyqtSlot(bool, name="on_start_clicked")
    def controlApp(self, checked):
        """ Docker docker_container should have:
            - Image: <url>/<image_name>:<tag> if tag is not provided, get latest
            - Name (unique)
            - Detach mode should be enabled
            - ports
            - environment 
        """
        # TODO having more statuses to be handled
        if self.container_info.status != 'RUNNING':
            self.start.setText('Starting')
            worker = Worker(containers_service.startContainer, self.container_info)
            worker.signals.result.connect(self.onAppStarted)
        else:
            self.start.setText('Stopping')
            worker = Worker(containers_service.stopContainer, self.container_info)
            worker.signals.result.connect(self.onAppStopped)
        worker.signals.error.connect(self.onFailure)
        threadpool.start(worker)

    def onAppStarted(self, container):
        self.container_info = container
        self.container_info.status = 'RUNNING'
        self.container_info.save()
        self.start.setText('Stop')
        # Todo: Add a green dot beside app's avatar

    def onAppStopped(self, status=True):
        self.container_info.status = 'STOPPED'
        self.container_info.save()
        self.start.setText('Start')

    def onFailure(self, exception):
        if isinstance(exception, DockerNotAvailableException):
            docker_utils.notify_docker_not_available()
        self.onAppStopped()

    def onAppClicked(self, event):
        if self.app_info.maximumHeight() == 0:
            self.animation = QPropertyAnimation(self.app_info, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.app_info_max_height)
            self.animation.start()
        else:
            self.animation = QPropertyAnimation(self.app_info, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setStartValue(self.app_info_max_height)
            self.animation.setEndValue(0)
            self.animation.start()
        QWidget.mouseReleaseEvent(self, event)
