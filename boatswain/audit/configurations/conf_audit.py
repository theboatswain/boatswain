from PyQt5.QtWidgets import QWidget

from boatswain.common.models.audit import Audit
from boatswain.common.models.audit_update import AuditUpdate
from boatswain.common.models.container import Container


class ConfAudit:

    def __init__(self, container: Container) -> None:
        super().__init__()
        self.container = container

    def getConfUpdate(self, conf_obj: AuditUpdate, parent=None) -> QWidget:
        raise NotImplementedError

    def getConfCreate(self, conf_obj: Audit, parent=None) -> QWidget:
        raise NotImplementedError

    def getConfDelete(self, conf_obj: Audit, parent=None) -> QWidget:
        raise NotImplementedError
