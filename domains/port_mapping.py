from peewee import *

from domains.base import BaseModel
from domains.container import Container


class PortMapping(BaseModel):
    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='ports')
    port = IntegerField()
    targetPort = IntegerField()
