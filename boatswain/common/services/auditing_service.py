from peewee import DoesNotExist

from boatswain.common.models.audit import Audit
from boatswain.common.models.audit_update import AuditUpdate
from boatswain.common.models.container import Container
from boatswain.common.utils.constants import AUDIT_CREATE, AUDIT_DELETE


def audit_update(container: Container, table: str, record_id: int, field: str, val_from, val_to):
    """
    Record the update action
    """
    try:
        # No need to record the changes from a new record
        audit = Audit.get((Audit.container == container) & (Audit.table == table) & (Audit.record_id == record_id))
        if audit.audit_mode == AUDIT_CREATE:
            return
    except DoesNotExist:
        pass
    try:
        audits = AuditUpdate.select().where((AuditUpdate.container == container) & (AuditUpdate.table == table)
                                            & (AuditUpdate.record_id == record_id))
        for audit in audits:
            if audit.field == field:
                if audit.value_to == audit.value_from:
                    audit.delete_instance()
                    return
                audit.value_to = val_to
                # val_from should be the old one that we had already recorded
                audit.save()
                return
    except DoesNotExist:
        pass
    new_audit = AuditUpdate(container=container, table=table, record_id=record_id, field=field, value_from=val_from,
                            value_to=val_to)
    new_audit.save()


def audit_create(container: Container, table: str, record_id: int):
    """
    Record the create action
    """
    try:
        Audit.get((Audit.container == container) & (Audit.table == table) & (Audit.record_id == record_id))
    except DoesNotExist:
        audit = Audit(container=container, table=table, record_id=record_id, audit_mode=AUDIT_CREATE)
        audit.save()


def audit_delete(container: Container, table: str, record_id: int):
    """
    Record the delete action
    if we delete an action that we just created before, then the created action will be deleted
    """
    try:
        audit = Audit.get((Audit.container == container) & (Audit.table == table) & (Audit.record_id == record_id))
        if audit.audit_mode == AUDIT_CREATE:
            audit.delete_instance()
    except DoesNotExist:
        audit = Audit(container=container, table=table, record_id=record_id, audit_mode=AUDIT_DELETE)
        audit.save()
