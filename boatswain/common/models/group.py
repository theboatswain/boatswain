from peewee import IntegerField, CharField, ForeignKeyField, BooleanField, FloatField

from boatswain.common.models.base import BaseModel
from boatswain.common.models.workspace import Workspace


class Group(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
    # for reorder the position of this container
    order = FloatField(index=True)
    is_default = BooleanField(default=False, index=True)
    workspace = ForeignKeyField(Workspace, backref='groups')
    expanded = BooleanField(default=True)
