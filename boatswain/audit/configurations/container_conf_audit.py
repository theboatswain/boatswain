from PyQt5.QtWidgets import QWidget

from boatswain.audit.configurations.conf_audit import ConfAudit
from boatswain.audit.template.conf_audit_handler import ConfAuditHandler
from boatswain.common.models.audit import Audit
from boatswain.common.models.audit_update import AuditUpdate


class ContainerConfAudit(ConfAudit):

    def getConfUpdate(self, conf_obj: AuditUpdate, parent=None) -> QWidget:
        conf_audit = ConfAuditHandler(parent, self.container).ui
        if conf_obj.field == "tag":
            conf_audit.name.setText("Image Tag changed from %s to %s" % (conf_obj.value_from, conf_obj.value_to))
        elif conf_obj.field == "memory_limit":
            conf_audit.name.setText("Amount of Memory allowed is limited to %sMB" % conf_obj.value_to)
        elif conf_obj.field == "cpu_limit":
            conf_audit.name.setText("Number of CPU allowed is limited to %s cpus" % conf_obj.value_to)
        elif conf_obj.field == "entrypoint":
            conf_audit.name.setText("Entrypoint changed to %s" % conf_obj.value_to)
        conf_audit.type.setText("Updated")
        conf_audit.type.setStyleSheet("background-color: yellow; padding: 2px 5px; color: black")
        return conf_audit

    def getConfCreate(self, conf_obj: Audit, parent=None) -> QWidget:
        pass

    def getConfDelete(self, conf_obj: Audit, parent=None) -> QWidget:
        pass
