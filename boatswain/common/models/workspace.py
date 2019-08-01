from peewee import IntegerField, CharField

from boatswain.common.models.base import BaseModel


class Workspace(BaseModel):
    id = IntegerField(primary_key=True)
    name = CharField()
