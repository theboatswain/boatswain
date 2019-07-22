from peewee import ForeignKeyField, CharField, IntegerField

from boatswain.common.models.base import BaseModel
from boatswain.common.models.container import Container


class PreferencesShortcut(BaseModel):
    id = IntegerField(primary_key=True)
    container = ForeignKeyField(Container, backref='preferences')
    # Name of this shortcut, will be showed in expanding window
    label = CharField()
    # Default value
    default_value = CharField()
    # type of the value. Can be Folder/File/Number or String
    pref_type = CharField()
    # type of this shortcut. Can be VolumeMapping/PortMapping/Environment
    shortcut = CharField()
    # depend on the shortcut type
    mapping_to = CharField()
    # order
    order = IntegerField()
