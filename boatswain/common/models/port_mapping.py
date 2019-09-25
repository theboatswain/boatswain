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
from peewee import IntegerField, ForeignKeyField, CharField

from boatswain.common.models.base import BaseModel
from boatswain.common.models.container import Container
from boatswain.common.utils.constants import STATUS_ADDED


class PortMapping(BaseModel):
    """ Model base for port mapping info """

    id = IntegerField(primary_key=True)
    # target container Id
    container = ForeignKeyField(Container, backref='ports')

    # Description about this port
    description = CharField(default='')

    # container port
    port = IntegerField()
    # protocol is either tcp, udp, or sctp.
    protocol = CharField(default='tcp')
    # host port
    target_port = IntegerField()

    status = IntegerField(index=True, default=STATUS_ADDED)
