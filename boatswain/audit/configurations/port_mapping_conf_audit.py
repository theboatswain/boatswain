from PyQt5.QtWidgets import QWidget

from boatswain.audit.configurations.conf_audit import ConfAudit
from boatswain.audit.template.conf_audit_handler import ConfAuditHandler
from boatswain.common.models.audit import Audit
from boatswain.common.models.audit_update import AuditUpdate
from boatswain.common.services import port_mapping_service
from boatswain.common.utils.utils import tr


class PortMappingConfAudit(ConfAudit):

    def getConfUpdate(self, conf_obj: AuditUpdate, parent=None) -> QWidget:
        conf_audit = ConfAuditHandler(parent, self.container, conf_obj).ui
        if conf_obj.field == "port":
            conf_audit.name.setText(tr("Container port changed from %s to %s") % (conf_obj.value_from, conf_obj.value_to))
        elif conf_obj.field == "target_port":
            conf_audit.name.setText(tr("Host port changed from %s to %s") % (conf_obj.value_from, conf_obj.value_to))
        elif conf_obj.field == "protocol":
            conf_audit.name.setText(tr("Protocol changed from from %s to %s") % (conf_obj.value_from, conf_obj.value_to))
        conf_audit.type.setText(tr("Updated"))
        conf_audit.type.setStyleSheet("background-color: yellow; padding: 2px 5px; color: black")
        return conf_audit

    def getConfCreate(self, conf: Audit, parent=None) -> QWidget:
        conf_audit = ConfAuditHandler(parent, self.container, conf).ui
        mapping = port_mapping_service.getPortMapping(int(conf.record_id))
        conf_audit.name.setText(tr("Mapping host port %s to container port %s") % (mapping.target_port, mapping.port))
        conf_audit.type.setText(tr("Created"))
        conf_audit.type.setStyleSheet("background-color: green; padding: 2px 5px; color: white")
        return conf_audit

    def getConfDelete(self, conf: Audit, parent=None) -> QWidget:
        conf_audit = ConfAuditHandler(parent, self.container, conf).ui
        port_mapping = port_mapping_service.getPortMapping(int(conf.record_id))
        conf_audit.name.setText(tr("Deleted port mapping %s:%s") % (port_mapping.target_port, port_mapping.port))
        conf_audit.type.setText(tr("Deleted"))
        conf_audit.type.setStyleSheet("background-color: red; padding: 2px 5px; color: white")
        return conf_audit
