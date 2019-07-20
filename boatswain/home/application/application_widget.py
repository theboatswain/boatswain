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

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QDialog, QMenu

from boatswain.common.exceptions.docker_exceptions import DockerNotAvailableException
from boatswain.common.models.container import Container
from boatswain.common.services import containers_service, data_transporter_service, boatswain_daemon
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils import docker_utils
from boatswain.common.utils.constants import ADD_APP_CHANNEL
from boatswain.home.application.application_widget_ui import AppWidgetUi
from boatswain.shortcut.preferences_shortcut import PreferencesShortcutWidget


class AppWidget:
    """ Class to customise app's widgets """

    _translate = QCoreApplication.translate
    template = 'AppWidget'

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = AppWidgetUi(parent, container, self)

        status = "Stop" if containers_service.isContainerRunning(container) else "Start"
        self.ui.status.setText(self._translate(self.template, status))
        self.ui.status.clicked.connect(self.controlApp)
        self.ui.name.setText(self._translate(self.template, self.container.name))

        self.ui.widget.mouseReleaseEvent = self.onAppClicked
        self.ui.contextMenuEvent = self.contextMenuEvent
        containers_service.listenContainerChange(container, self.onContainerChange)
        boatswain_daemon.listen('container', 'start', self.onContainerStart)
        boatswain_daemon.listen('container', 'stop', self.onContainerStop)

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
        # Todo: Handle more exceptions

    def onAppClicked(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.ui.advanced_app.toggleWindow()

    def onPreferenceShortcutClicked(self):
        dialog = QDialog(self)
        dialog.ui = PreferencesShortcutWidget(dialog, self.ui.container_info)
        dialog.exec_()

    def onContainerStart(self, event):
        if containers_service.isInstanceOf(self.container, event['id']):
            self.ui.status.setText(self._translate(self.template, 'Stop'))
            # Todo: Add a green dot beside app's avatar

    def onContainerStop(self, event):
        if containers_service.isInstanceOf(self.container, event['id']):
            self.ui.status.setText(self._translate(self.template, 'Start'))

    def contextMenuEvent(self, event):
        menu = QMenu(self.ui)
        add_action = menu.addAction(self._translate(self.template, 'Add...'))
        add_action.triggered.connect(lambda: data_transporter_service.fire(ADD_APP_CHANNEL, True))
        menu.addSeparator()
        terminal = menu.addAction(self._translate(self.template, 'Connect to terminal'))
        terminal.triggered.connect(lambda: containers_service.connectToContainer(self.container))
        menu.addAction(self._translate(self.template, 'Open log'))
        menu.addSeparator()
        conf = menu.addAction(self._translate(self.template, 'Configuration'))
        conf.triggered.connect(lambda: self.ui.advanced_app.onAdvancedConfigurationClicked())
        pref_shortcut = menu.addAction(self._translate(self.template, 'Preferences shortcut'))
        pref_shortcut.triggered.connect(self.onPreferenceShortcutClicked)
        menu.addSeparator()
        menu.addAction(self._translate(self.template, 'Restart'))
        menu.addAction(self._translate(self.template, 'Reset'))
        menu.addAction(self._translate(self.template, 'Delete'))
        menu.exec_(self.ui.mapToGlobal(event.pos()))

    def onContainerChange(self, data=None):
        self.ui.name.setText(self._translate(self.template, self.container.name))
