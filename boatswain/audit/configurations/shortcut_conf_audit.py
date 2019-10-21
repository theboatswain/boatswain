from PyQt5.QtWidgets import QWidget
from boatswain.common.services import shortcut_service

from boatswain.audit.configurations.conf_audit import ConfAudit
from boatswain.audit.template.conf_audit_handler import ConfAuditHandler
from boatswain.common.models.audit import Audit
from boatswain.common.models.audit_update import AuditUpdate


class ShortcutConfAudit(ConfAudit):

    def getConfUpdate(self, conf: AuditUpdate, parent=None) -> QWidget:
        conf_audit = ConfAuditHandler(parent, self.container).ui
        shortcut = shortcut_service.getShortcut(int(conf.record_id))
        if shortcut.shortcut == 'Volume Mount':
            conf_audit.name.setText("%s changed to %s" % (shortcut.label, conf.value_to))
        else:
            conf_audit.name.setText("%s changed from %s to %s" % (shortcut.label, conf.value_from, conf.value_to))
        conf_audit.type.setText("Updated")
        conf_audit.type.setStyleSheet("background-color: yellow; padding: 2px 5px; color: black")
        return conf_audit

    def getConfCreate(self, conf_obj: Audit, parent=None) -> QWidget:
        pass

    def getConfDelete(self, conf_obj: Audit, parent=None) -> QWidget:
        pass
