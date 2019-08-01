from peewee import IntegerField, CharField, ForeignKeyField

from boatswain.common.models.base import BaseModel
from boatswain.common.models.workspace import Workspace


class Group(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    workspace = ForeignKeyField(Workspace, backref='groups')
