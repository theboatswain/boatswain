from common.models.base import BaseModel, ForeignKeyField, CharField
from common.models.container import Container


class Configuration(BaseModel):
    """This class for saving any other configurations"""
    name = CharField()
    container = ForeignKeyField(Container, backref='configurations')
    value = CharField()
