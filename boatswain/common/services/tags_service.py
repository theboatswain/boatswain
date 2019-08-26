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

from typing import List

from boatswain.common.models.container import Container
from boatswain.common.models.tag import Tag


def getTags(container: Container) -> List[Tag]:
    return Tag.select().where(Tag.container == container)


def cloneAll(from_container: Container, to_container: Container):
    for tag in getTags(from_container):
        tag.id = None
        tag.container = to_container
        tag.save()


def deleteAll(container: Container):
    Tag.delete().where(Tag.container == container).execute()
