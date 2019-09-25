from peewee import IntegerField, ForeignKeyField, CharField

from boatswain.common.models.base import BaseModel
from boatswain.common.models.container import Container


class Audit(BaseModel):
    """ Model object that record the update action to the container's related information"""

    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='audits')
    # Create/Delete
    audit_mode = CharField()
    table = CharField(index=True)
    record_id = IntegerField(index=True)
