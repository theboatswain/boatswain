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
