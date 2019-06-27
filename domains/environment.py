from peewee import *

from domains.base import BaseModel
from domains.container import Container


class Environment(BaseModel):
    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='environments')
    name = CharField()
    value = CharField()
