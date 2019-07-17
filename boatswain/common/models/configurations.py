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
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#
from peewee import CharField, ForeignKeyField

from boatswain.common.models.base import BaseModel
from boatswain.common.models.container import Container


class Configuration(BaseModel):
    """This class for saving any other configurations"""
    name = CharField()
    container = ForeignKeyField(Container, backref='configurations')
    value = CharField()
