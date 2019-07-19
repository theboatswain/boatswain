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

from PyQt5.QtCore import QCoreApplication, Qt, QPropertyAnimation
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QDialog

from boatswain.common.exceptions.docker_exceptions import DockerNotAvailableException
from boatswain.common.models.container import Container
from boatswain.common.services import containers_service
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils import docker_utils
from boatswain.common.utils.custom_ui import ReloadableWidget
from boatswain.home.application.application_widget_ui import AppWidgetUi
from boatswain.shortcut.preferences_shortcut import PreferencesShortcutWidget


class AppWidget(ReloadableWidget):
    """ Class to customise app's widgets """

    _translate = QCoreApplication.translate
    template = 'AppWidget'
    animation: QPropertyAnimation

    def reloadData(self):
        self.ui.name.setText(self._translate(self.template, self.container.name))
        self.ui.advanced_app.reloadData()

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = AppWidgetUi(parent, container)

        status = "Stop" if containers_service.isContainerRunning(container) else "Start"
        self.ui.status.setText(self._translate(self.template, status))
        self.ui.status.clicked.connect(self.controlApp)
        self.reloadData()

    def controlApp(self):
        if not containers_service.isContainerRunning(self.container):
            self.ui.status.setText('Starting')
            worker = Worker(containers_service.startContainer, self.container)
            worker.signals.result.connect(self.onAppStarted)
        else:
            self.ui.status.setText('Stopping')
            worker = Worker(containers_service.stopContainer, self.container)
        worker.signals.error.connect(self.onFailure)
        threadpool.start(worker)

    def onAppStarted(self, container):
        self.container = container
        self.container.save()
        self.ui.status.setText('Stop')

    def onFailure(self, exception):
        if isinstance(exception, DockerNotAvailableException):
            docker_utils.notifyDockerNotAvailable()

    def onAppClicked(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if self.ui.advanced_app.maximumHeight() == 0:
                self.animation = QPropertyAnimation(self.ui.advanced_app, b"maximumHeight")
                self.animation.setDuration(300)
                self.animation.setStartValue(0)
                self.animation.setEndValue(self.ui.app_info_max_height)
                self.animation.start()
            else:
                self.animation = QPropertyAnimation(self.ui.advanced_app, b"maximumHeight")
                self.animation.setDuration(300)
                self.animation.setStartValue(self.ui.app_info_max_height)
                self.animation.setEndValue(0)
                self.animation.start()

    def onPreferenceShortcutClicked(self):
        dialog = QDialog(self)
        dialog.ui = PreferencesShortcutWidget(dialog, self.ui.container_info)
        dialog.exec_()

    def onContainerStart(self, event):
        if containers_service.isInstanceOf(self.container, event['id']):
            self.ui.status.setText('Stop')
            # Todo: Add a green dot beside app's avatar

    def onContainerStop(self, event):
        if containers_service.isInstanceOf(self.container, event['id']):
            self.ui.status.setText('Start')
