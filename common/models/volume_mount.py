from peewee import *

from common.models.base import BaseModel
from common.models.container import Container


class VolumeMount(BaseModel):
    """ Model base for storing info of mounted volumes """

    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='volumes')
    hostPath = CharField()
    containerPath = CharField()
    description = CharField(default='')
