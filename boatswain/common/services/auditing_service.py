import time

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
                if str(val_to) == audit.value_from:
                    audit.delete_instance()
                    return
                audit.value_to = val_to
                # val_from should be the old one that we had already recorded
                audit.save()
                return
    except DoesNotExist:
        pass
    if str(val_from) == str(val_to):
        return
    new_audit = AuditUpdate(container=container, table=table, record_id=record_id, field=field, value_from=val_from,
                            value_to=val_to, time=time.time())
    new_audit.save()


def audit_create(container: Container, table: str, record_id: int):
    """
    Record the create action
    """
    try:
        Audit.get((Audit.container == container) & (Audit.table == table) & (Audit.record_id == record_id))
    except DoesNotExist:
        audit = Audit(container=container, table=table, record_id=record_id, audit_mode=AUDIT_CREATE, time=time.time())
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
        audit = Audit(container=container, table=table, record_id=record_id, audit_mode=AUDIT_DELETE, time=time.time())
        audit.save()


def getAudits(container: Container):
    result = list(Audit.select().where(Audit.container == container))
    result += list(AuditUpdate.select().where(AuditUpdate.container == container))
    result.sort(key=lambda x: x.time)
    return result


def cleanAudits(container: Container):
    Audit.delete().where(Audit.container == container).execute()
    AuditUpdate.delete().where(AuditUpdate.container == container).execute()


def containerChangingLevel(container: Container) -> int:
    """
    Level 0: no need to do anything
    Level 1: be able to merge
    Level 2: unable to merge
    """
    try:
        Audit.get(Audit.container == container)
        return 1
    except DoesNotExist:
        pass
    audits = AuditUpdate.select().where(AuditUpdate.container == container)
    for audit in audits:
        if audit.field == 'tag':
            return 2
    for audit in audits:
        if audit.field not in ['description', 'label']:
            return 1
    return 0
