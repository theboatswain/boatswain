from peewee import *

from domains.base import BaseModel
from domains.container import Container


class VolumeMount(BaseModel):
    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='volumes')
    hostPath = CharField()
    containerPath = CharField()
