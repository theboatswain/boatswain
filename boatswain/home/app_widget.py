#  This file is part of Boatswain.
#
#      Boatswain is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Boatswain is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt, QPropertyAnimation, pyqtSlot
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout, QSizePolicy, QFrame, QMenu, QDialog

from boatswain.common.exceptions.docker_exceptions import DockerNotAvailableException
from boatswain.common.models.container import Container
from boatswain.common.services import boatswain_daemon, data_transporter_service, containers_service
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils import text_utils, docker_utils
from boatswain.common.utils.app_avatar import AppAvatar
from boatswain.common.utils.constants import ADD_APP_CHANNEL
from boatswain.common.utils.custom_ui import BQSizePolicy, ReloadableWidget
from boatswain.home.advanced_app_widget import AdvancedAppWidget
from boatswain.shortcut.preferences_shortcut import PreferencesShortcutWidget


class AppWidget(ReloadableWidget):
    """ Class to customise app's widgets """

    def reloadData(self):
        self.name.setText(self._translate("widget", self.container_info.name))
        self.app_info.reloadData()

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
        self._translate = QCoreApplication.translate

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

        self.status = QPushButton(widget)
        self.status.setObjectName("start")
        self.status.setFlat(True)
        self.status.setStyleSheet("border: 1px solid #999999; padding: 1px 10px; border-radius: 2px")
        self.horizontal_layout.addWidget(self.status)

        self.app_info = AdvancedAppWidget(widget, container)
        self.app_info_max_height = self.app_info.sizeHint().height() + 10
        self.app_info.setMaximumHeight(0)

        self.vertical_layout.addWidget(self.app_info)
        self.container_info = container

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        self.vertical_layout.addWidget(line)

        status = "Stop" if containers_service.isContainerRunning(container) else "Start"
        self.status.setText(self._translate("widget", status))

        boatswain_daemon.listen('container', 'start', self.onContainerStart)
        boatswain_daemon.listen('container', 'stop', self.onContainerStop)
        QMetaObject.connectSlotsByName(self)

        self.reloadData()

    @pyqtSlot(bool, name="on_start_clicked")
    def controlApp(self, checked):
        """ Docker docker_container should have:
            - Image: <url>/<image_name>:<tag> if tag is not provided, get latest
            - Name (unique)
            - Detach mode should be enabled
            - ports
            - environment
        """
        if not containers_service.isContainerRunning(self.container_info):
            self.status.setText('Starting')
            worker = Worker(containers_service.startContainer, self.container_info)
            worker.signals.result.connect(self.onAppStarted)
        else:
            self.status.setText('Stopping')
            worker = Worker(containers_service.stopContainer, self.container_info)
        worker.signals.error.connect(self.onFailure)
        threadpool.start(worker)

    def onAppStarted(self, container):
        self.container_info = container
        self.container_info.save()
        self.status.setText('Stop')

    def onFailure(self, exception):
        if isinstance(exception, DockerNotAvailableException):
            docker_utils.notifyDockerNotAvailable()

    def onAppClicked(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
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

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        add_action = menu.addAction("Add...")
        add_action.triggered.connect(lambda: data_transporter_service.fire(ADD_APP_CHANNEL, True))
        menu.addSeparator()
        terminal = menu.addAction("Connect to terminal")
        terminal.triggered.connect(lambda: containers_service.connectToContainer(self.container_info))
        menu.addAction("Open log")
        menu.addSeparator()
        conf = menu.addAction("Configuration")
        conf.triggered.connect(lambda: self.app_info.onAdvancedConfigurationClicked())
        pref_shortcut = menu.addAction("Preferences shortcut")
        pref_shortcut.triggered.connect(self.onPreferenceShortcutClicked)
        menu.addSeparator()
        menu.addAction("Restart")
        menu.addAction("Reset")
        menu.addAction("Delete")
        menu.exec_(self.mapToGlobal(event.pos()))

    def onPreferenceShortcutClicked(self):
        dialog = QDialog(self)
        dialog.ui = PreferencesShortcutWidget(dialog, self.container_info)
        dialog.exec_()

    def onContainerStart(self, event):
        if containers_service.isInstanceOf(self.container_info, event['id']):
            self.status.setText('Stop')
            # Todo: Add a green dot beside app's avatar

    def onContainerStop(self, event):
        if containers_service.isInstanceOf(self.container_info, event['id']):
            self.status.setText('Start')
