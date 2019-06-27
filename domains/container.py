from peewee import *

from domains.base import BaseModel


class Container(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    tag = CharField()
    description = TextField()
    status = IntegerField()
    avatar = CharField(default='')
