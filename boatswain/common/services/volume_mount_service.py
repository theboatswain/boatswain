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
from boatswain.common.models.volume_mount import VolumeMount


def getVolumeMounts(container: Container) -> List[VolumeMount]:
    return VolumeMount.select().where(VolumeMount.container == container)


def cloneAll(from_container: Container, to_container: Container):
    for volume_mount in getVolumeMounts(from_container):
        volume_mount.id = None
        volume_mount.container = to_container
        volume_mount.save()


def deleteAll(container: Container):
    VolumeMount.delete().where(VolumeMount.container == container).execute()
