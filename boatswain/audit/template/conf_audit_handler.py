from boatswain.audit.template.conf_audit_ui import ConfAuditUi
from boatswain.common.models.container import Container


class ConfAuditHandler(object):

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = ConfAuditUi(parent, self)
