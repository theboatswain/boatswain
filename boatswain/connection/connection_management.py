from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QDialogButtonBox
from docker import APIClient

from boatswain.common.exceptions.docker_exceptions import DockerNotAvailableException
from boatswain.common.services import global_preference_service, docker_service
from boatswain.common.utils.constants import PROTOCOL_KEY
from boatswain.common.utils.utils import tr
from boatswain.connection.connection_management_ui import ConnectionManagementUi


class ConnectionManagement(QObject):
    time = 1
    status = False
    conf_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        current_protocol = global_preference_service.getCurrentDockerURL()
        self.dialog = QDialog(parent)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.ui = ConnectionManagementUi(self.dialog)
        self.dialog.ui = self.ui
        self.ui.url.setText(current_protocol)
        self.ui.button_box.accepted.connect(self.checkConnection)
        self.checkConnection()

    def checkConnection(self):
        if self.status:
            self.saveConfiguration()
            self.conf_updated.emit()
            return self.dialog.accept()
        docker_service.client.api = APIClient(base_url=self.ui.url.text())
        try:
            docker_service.ping()
            self.ui.message.setText(tr("Connection successful!!!"))
            self.ui.button_box.button(QDialogButtonBox.Ok).setText(tr("Save"))
            self.status = True
        except DockerNotAvailableException:
            mess = tr("We are unable to connect to the Docker upstream!!!")
            if self.time > 1:
                mess += tr(" (time %d)") % self.time
            self.ui.message.setText(mess)
            self.time += 1
            self.status = False
        self.ui.message.repaint()

    def saveConfiguration(self):
        global_preference_service.setPreference(PROTOCOL_KEY, self.ui.url.text())

    def show(self):
        self.dialog.exec_()
