#  This file is part of Boatswain.
#
#      Boatswain<https://github.com/theboatswain> is free software: you can redistribute it and/or modify
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
from boatswain.common.models.port_mapping import PortMapping
from boatswain.common.utils.constants import STATUS_ADDED


def getPortMappings(container: Container) -> List[PortMapping]:
    return PortMapping.select().where((PortMapping.container == container) & (PortMapping.status == STATUS_ADDED))


def cloneAll(from_container: Container, to_container: Container):
    for port_mapping in getPortMappings(from_container):
        port_mapping.id = None
        port_mapping.container = to_container
        port_mapping.save()


def deleteAll(container: Container):
    PortMapping.delete().where(PortMapping.container == container).execute()


def getPortMapping(port_id: int):
    return PortMapping.get(port_id)
