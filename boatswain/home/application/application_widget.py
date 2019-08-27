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
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5.QtCore import QCoreApplication, Qt, QMimeData, QTimer, QPoint
from PyQt5.QtGui import QMouseEvent, QDrag, QPixmap, QDragEnterEvent, QDragLeaveEvent, QDragMoveEvent, QRegion
from PyQt5.QtWidgets import QMenu, QMessageBox, QWidget
from docker.errors import APIError

from boatswain.common.exceptions.docker_exceptions import DockerNotAvailableException
from boatswain.common.models.container import Container
from boatswain.common.services import containers_service, data_transporter_service, boatswain_daemon, workspace_service
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils import docker_utils
from boatswain.common.utils.constants import ADD_APP_CHANNEL, SHORTCUT_CONF_CHANGED_CHANNEL, CONTAINER_CHANNEL
from boatswain.home.application.application_widget_ui import AppWidgetUi
from boatswain.shortcut.preferences_shortcut_config import PreferencesShortcutConfig


class AppWidget:
    """ Class to customise app's widgets """

    _translate = QCoreApplication.translate
    template = 'AppWidget'

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = AppWidgetUi(parent, container, self)

        self.autoSetContainerStatus()
        self.ui.status.clicked.connect(self.controlApp)
        self.ui.name.setText(self._translate(self.template, self.container.name))

        self.ui.widget.mouseReleaseEvent = self.onMouseReleased
        self.ui.widget.mousePressEvent = self.mousePressEvent
        self.ui.dragEnterEvent = self.dragEnterEvent
        self.ui.dragLeaveEvent = self.dragLeaveEvent
        self.ui.dragMoveEvent = self.dragMoveEvent
        self.ui.contextMenuEvent = self.contextMenuEvent
        boatswain_daemon.listen('container', 'start', self.onContainerStart)
        boatswain_daemon.listen('container', 'stop', self.onContainerStop)
        boatswain_daemon.listen('container', 'die', self.onContainerStop)
        containers_service.listen(self.container, 'name', lambda x: self.ui.name.setText(x))
        self.is_mouse_released = True
        self.ui.setAcceptDrops(True)

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
        self.autoSetContainerStatus()

    def onFailure(self, exception):
        if isinstance(exception, DockerNotAvailableException):
            docker_utils.notifyDockerNotAvailable()
        if isinstance(exception, APIError):
            message = exception.response.json()
            docker_utils.notifyDockerException(message['message'])
        self.autoSetContainerStatus()
        # Todo: Handle more exceptions

    def onMouseReleased(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_mouse_released = True
            self.ui.advanced_app.toggleWindow()

    def onPreferenceShortcutClicked(self):
        shortcut = PreferencesShortcutConfig(self.ui, self.ui.container_info)
        shortcut.show()

    def onContainerStart(self, event):
        if containers_service.isInstanceOf(self.container, event['id']):
            self.autoSetContainerStatus()
            # Todo: Add a green dot beside app's avatar

    def onContainerStop(self, event):
        if containers_service.isInstanceOf(self.container, event['id']):
            self.autoSetContainerStatus()

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
        conf.triggered.connect(self.ui.advanced_app.onAdvancedConfigurationClicked)
        pref_shortcut = menu.addAction(self._translate(self.template, 'Preferences shortcut'))
        pref_shortcut.triggered.connect(self.onPreferenceShortcutClicked)
        menu.addSeparator()
        clone_to = QMenu(self._translate(self.template, 'Clone to...'), self.ui)
        clone_to.addAction(self._translate(self.template, 'Unspecified workspace'))
        for workspace in workspace_service.getWorkspaces():
            clone_to.addAction(workspace.name)
        clone_to.triggered.connect(self.cloneContainer)
        menu.addMenu(clone_to)
        menu.addSeparator()
        restart = menu.addAction(self._translate(self.template, 'Restart'))
        restart.triggered.connect(self.restartContainer)
        reset = menu.addAction(self._translate(self.template, 'Reset'))
        reset.triggered.connect(self.resetContainer)
        delete = menu.addAction(self._translate(self.template, 'Delete'))
        delete.triggered.connect(self.deleteContainer)
        menu.exec_(self.ui.mapToGlobal(event.pos()))

    def restartContainer(self):
        if containers_service.isContainerRunning(self.container):
            self.ui.status.setText('Stopping')
            worker = Worker(containers_service.stopContainer, self.container)
            worker.signals.result.connect(self.restartContainer)
        else:
            self.ui.status.setText('Starting')
            containers_service.startContainer(self.container)
            worker = Worker(containers_service.startContainer, self.container)
            worker.signals.result.connect(self.onAppStarted)

        worker.signals.error.connect(self.onFailure)
        threadpool.start(worker)

    def cloneContainer(self, action):
        clone_to_workspace = action.text()
        if clone_to_workspace == 'Unspecified workspace':
            workspace = workspace_service.getDefaultWorkspace()
        else:
            workspace = workspace_service.getWorkspace(clone_to_workspace)
        worker = Worker(containers_service.cloneContainer, self.container, workspace)
        worker.signals.result.connect(lambda x: data_transporter_service.fire(CONTAINER_CHANNEL, x))
        threadpool.start(worker)

    def autoSetContainerStatus(self):
        status = "Stop" if containers_service.isContainerRunning(self.container) else "Start"
        self.ui.status.setText(self._translate(self.template, status))

    def deleteContainer(self):
        message = self._translate(self.template, "Are you sure you want to delete this container? All configurations "
                                                 "you made for it will be deleted also!")
        button_reply = QMessageBox.question(self.ui, 'Delete container', message,
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if button_reply == QMessageBox.Ok:
            containers_service.deleteContainer(self.container)
            self.ui.deleteLater()

    def resetContainer(self):
        message = self._translate(self.template, "Are you sure you want to reset this container? All configurations "
                                                 "you made for it will be lost!")
        button_reply = QMessageBox.question(self.ui, 'Reset container', message,
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if button_reply == QMessageBox.Ok:
            containers_service.deleteConfigurations(self.container)
            containers_service.fire(self.container, SHORTCUT_CONF_CHANGED_CHANNEL, True)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_mouse_released = False
            timer = QTimer(self.ui)
            timer.setSingleShot(True)
            pos = event.pos()
            timer.timeout.connect(lambda: self.startDragging(pos))
            timer.start(200)

    def startDragging(self, pos):
        if not self.is_mouse_released:
            drag = QDrag(self.ui.widget)
            mime_data = QMimeData()
            mime_data.setText(str(self.container.id))
            widget_pixmap = QPixmap(self.ui.widget.size())
            widget_pixmap.fill(Qt.transparent)
            self.ui.widget.render(widget_pixmap, QPoint(), QRegion(), QWidget.DrawChildren)
            drag.setMimeData(mime_data)
            drag.setPixmap(widget_pixmap)
            drag.setHotSpot(pos)
            drag.exec_()

    def getDragLocation(self, pos: QPoint):
        pos_y = pos.y()
        height = self.ui.geometry().height()
        if pos_y > height * 1 / 2:
            return -1
        return 0

    def cleanDragEffects(self):
        self.ui.color_line.hide()
        self.ui.line.show()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            data: str = event.mimeData().text()
            if data.isdigit() and int(data) != self.container.id:
                event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        self.cleanDragEffects()
        loc = self.getDragLocation(event.pos())
        if loc == -1:
            self.ui.color_line.show()
            self.ui.line.hide()

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.cleanDragEffects()
