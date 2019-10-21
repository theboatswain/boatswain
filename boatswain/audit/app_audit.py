from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog

from boatswain.audit.app_audit_ui import AppAuditUi
from boatswain.audit.configurations.conf_audit_factory import ConfAuditFactory
from boatswain.common.models.container import Container
from boatswain.common.services import auditing_service


class AppAudit(QObject):
    start_old_conf = pyqtSignal()
    start_new_conf = pyqtSignal()

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.dialog = QDialog(parent)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.ui = AppAuditUi(self.dialog, container, self)
        self.dialog.ui = self.ui
        audit_factory = ConfAuditFactory()
        audits = auditing_service.getAudits(container)
        for audit in audits:
            widget = audit_factory.getConfAudit(audit, container, self.dialog)
            self.ui.app_list_layout.addWidget(widget)
        self.ui.cancel.clicked.connect(self.cancel)
        self.ui.old_conf.clicked.connect(self.startOldConf)
        self.ui.merge.clicked.connect(self.merge)

    def show(self):
        self.dialog.exec_()

    def cancel(self):
        self.dialog.close()

    def startOldConf(self):
        self.start_old_conf.emit()
        self.dialog.accept()

    def merge(self):
        auditing_service.cleanAudits(self.container)
        self.start_new_conf.emit()
        self.dialog.accept()
