from boatswain.audit.template.conf_audit_ui import ConfAuditUi
from boatswain.common.models import tables
from boatswain.common.models.audit_update import AuditUpdate
from boatswain.common.models.container import Container
from boatswain.common.services import containers_service
from boatswain.common.utils import constants
from boatswain.common.utils.constants import SHORTCUT_CONF_CHANGED_CHANNEL


class ConfAuditHandler(object):

    def __init__(self, parent, container: Container, conf_obj) -> None:
        self.container = container
        self.ui = ConfAuditUi(parent, self)
        self.conf_obj = conf_obj
        self.ui.undo.clicked.connect(self.undo)

    def undo(self):
        if self.conf_obj.table == self.container.tableName():
            # We have to check the container object because the value of this object is still accessing from many places
            # So, in case of undo, we need to update both the in-memory and in-db as well
            # And, if the object table is container, the type of it will always be AuditUpdate
            setattr(self.container, self.conf_obj.field, self.conf_obj.value_from)
            self.container.save()
        else:
            for table in tables.db_tables:
                if self.conf_obj.table.lower() != table._meta.name.lower():
                    continue
                obj_instance = table.get(table.id == self.conf_obj.record_id)
                if isinstance(self.conf_obj, AuditUpdate):
                    setattr(obj_instance, self.conf_obj.field, self.conf_obj.value_from)
                    obj_instance.save()
                else:
                    if self.conf_obj.audit_mode == constants.AUDIT_CREATE:
                        obj_instance.delete_instance()
                    elif self.conf_obj.audit_mode == constants.AUDIT_DELETE:
                        setattr(obj_instance, "status", constants.STATUS_ADDED)
                        obj_instance.save()

                if self.conf_obj.table == "PreferencesShortcut":
                    containers_service.fire(self.container, SHORTCUT_CONF_CHANGED_CHANNEL)
                break

        self.conf_obj.delete_instance()
        self.ui.parentWidget().layout().removeWidget(self.ui)
        self.ui.deleteLater()
