from PyQt5.QtWidgets import QWidget

from boatswain.audit.configurations.conf_audit import ConfAudit
from boatswain.audit.template.conf_audit_handler import ConfAuditHandler
from boatswain.common.models.audit import Audit
from boatswain.common.models.audit_update import AuditUpdate
from boatswain.common.services import environment_service


class EnvironmentConfAudit(ConfAudit):

    def getConfUpdate(self, conf_obj: AuditUpdate, parent=None) -> QWidget:
        conf_audit = ConfAuditHandler(parent, self.container, conf_obj).ui
        mapping = environment_service.getEnvironment(int(conf_obj.record_id))
        if conf_obj.field == "name":
            conf_audit.name.setText("Env name changed from %s to %s" % (conf_obj.value_from, conf_obj.value_to))
        elif conf_obj.field == "value":
            conf_audit.name.setText("Env %s set value to %s" % (mapping.name, conf_obj.value_to))
        conf_audit.type.setText("Updated")
        conf_audit.type.setStyleSheet("background-color: yellow; padding: 2px 5px; color: black")
        return conf_audit

    def getConfCreate(self, conf: Audit, parent=None) -> QWidget:
        conf_audit = ConfAuditHandler(parent, self.container, conf).ui
        mapping = environment_service.getEnvironment(int(conf.record_id))
        conf_audit.name.setText("Set env %s = %s" % (mapping.name, mapping.value))
        conf_audit.type.setText("Created")
        conf_audit.type.setStyleSheet("background-color: green; padding: 2px 5px; color: white")
        return conf_audit

    def getConfDelete(self, conf: Audit, parent=None) -> QWidget:
        conf_audit = ConfAuditHandler(parent, self.container, conf).ui
        mapping = environment_service.getEnvironment(int(conf.record_id))
        conf_audit.name.setText("Deleted env %s" % mapping.name)
        conf_audit.type.setText("Deleted")
        conf_audit.type.setStyleSheet("background-color: red; padding: 2px 5px; color: white")
        return conf_audit
