from peewee import *

from common.models.base import BaseModel
from common.models.container import Container


class PortMapping(BaseModel):
    """ Model base for port mapping info """

    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='ports')
    port = IntegerField()
    targetPort = IntegerField()
