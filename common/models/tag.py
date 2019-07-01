from peewee import IntegerField, ForeignKeyField, CharField

from common.models.base import BaseModel
from common.models.container import Container


class Tag(BaseModel):
    """ Model object represents for a docker tags"""

    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='tags')
    name = CharField()
    size = IntegerField()
