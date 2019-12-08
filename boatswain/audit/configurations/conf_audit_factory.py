from PyQt5.QtWidgets import QWidget

from boatswain.audit.configurations.container_conf_audit import ContainerConfAudit
from boatswain.audit.configurations.environment_conf_audit import EnvironmentConfAudit
from boatswain.audit.configurations.port_mapping_conf_audit import PortMappingConfAudit
from boatswain.audit.configurations.shortcut_conf_audit import ShortcutConfAudit
from boatswain.audit.configurations.volume_mount_conf_audit import VolumeMountConfAudit
from boatswain.common.models.audit import Audit
from boatswain.common.models.audit_update import AuditUpdate
from boatswain.common.models.container import Container
from boatswain.common.utils.constants import AUDIT_CREATE


class ConfAuditFactory(object):

    def __init__(self):
        super().__init__()

    def getConfAudit(self, object_audit, container: Container, parent=None) -> QWidget:
        conf_audit = self.getConfAuditByName(getattr(object_audit, "table"), container)
        if isinstance(object_audit, AuditUpdate):
            return conf_audit.getConfUpdate(object_audit, parent)
        if isinstance(object_audit, Audit):
            if object_audit.audit_mode == AUDIT_CREATE:
                return conf_audit.getConfCreate(object_audit, parent)
            return conf_audit.getConfDelete(object_audit, parent)
        return None

    def getConfAuditByName(self, table_name, container):
        if table_name == "Container":
            return ContainerConfAudit(container)
        elif table_name == "PreferencesShortcut":
            return ShortcutConfAudit(container)
        elif table_name == 'PortMapping':
            return PortMappingConfAudit(container)
        elif table_name == 'VolumeMount':
            return VolumeMountConfAudit(container)
        elif table_name == 'Environment':
            return EnvironmentConfAudit(container)
