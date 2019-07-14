from peewee import *

from common.models.base import BaseModel
from common.models.container import Container


class VolumeMount(BaseModel):
    """ Model base for storing info of mounted volumes """

    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='volumes')
    host_path = CharField()
    container_path = CharField()
    mode = CharField(default='rw')
    description = CharField(default='')
