from peewee import *

from common.models.base import BaseModel
from common.models.container import Container


class Environment(BaseModel):
    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='environments')
    name = CharField()
    value = CharField()
    description = CharField(default='')
