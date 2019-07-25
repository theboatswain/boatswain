from peewee import IntegerField, CharField

from boatswain.common.models.base import BaseModel


class Preference(BaseModel):
    """This class for saving any global configurations"""
    id = IntegerField(primary_key=True)
    name = CharField()
    value = CharField()
