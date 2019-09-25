from peewee import IntegerField, ForeignKeyField, CharField

from boatswain.common.models.base import BaseModel
from boatswain.common.models.container import Container


class AuditUpdate(BaseModel):
    """ Model object represents for a docker container"""

    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='audits')
    table = CharField(index=True)
    record_id = IntegerField(index=True)
    field = CharField()
    value_from = CharField()
    value_to = CharField()
