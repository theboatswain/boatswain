#  This file is part of Boatswain.
#
#      Boatswain is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Boatswain is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

from peewee import ForeignKeyField, CharField, IntegerField, BooleanField, TextField

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
    # enable/disable this shortcut
    enabled = BooleanField(default=True)
    # description about this preference shortcut
    description = TextField(default='')
