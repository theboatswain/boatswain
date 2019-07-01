from peewee import *

from common.models.base import BaseModel


class Container(BaseModel):
    """ Model object represents for a docker container"""

    id = IntegerField(primary_key=True)
    name = CharField()
    tag = CharField()
    description = TextField()
    status = IntegerField()
    avatar = CharField(default='')
    repo = CharField(default='dockerhub')
