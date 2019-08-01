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
from peewee import IntegerField, CharField, TextField, FloatField, ForeignKeyField

from boatswain.common.models.base import BaseModel
from boatswain.common.models.group import Group


class Container(BaseModel):
    """ Model object represents for a docker container"""

    id = IntegerField(primary_key=True)
    # container short hash Id, ex: 8932a3a78c7f
    container_id = CharField(default='')
    # docker container name
    # image name, ex: mongo
    image_name = CharField()

    # customisable name
    name = CharField(default='')
    # image tag, ex: 1.0
    tag = CharField()
    # a short info that describes about app/soft/tool...
    description = TextField()
    # avatar for the container
    avatar = CharField(default='')
    # docker registry, default is docker hub, users can also use a custom registry
    repo = CharField(default='dockerhub')
    # limit amount of memory for this container
    memory_limit = IntegerField(default=0)
    # unit of the memory limit MB/GB
    memory_limit_unit = CharField(default='MB')
    # limit number of cpus for this container
    cpu_limit = FloatField(default=0.0)
    # unit of the cpu limit CPUs/Period/Quota
    cpu_limit_unit = CharField(default='CPUs')

    # overwriting the default behavior
    entrypoint = CharField(default='')

    # for reorder the position of this container
    order = IntegerField()

    group = ForeignKeyField(Group, backref='containers')
