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

import os

from peewee import SqliteDatabase, Model

from boatswain.common.utils.constants import APP_DATA_DIR, APP_DB

db = SqliteDatabase(os.path.join(APP_DATA_DIR, APP_DB))
tables = {}


class BaseModel(Model):
    """ Base model for boat swain """

    def __init__(self, *args, **kwargs):
        tables[self.__class__.__name__] = self
        super().__init__(*args, **kwargs)

    class Meta:
        database = db

    def tableName(self):
        return self.__class__.__name__
