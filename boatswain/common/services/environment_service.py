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
from boatswain.common.models.environment import Environment
from boatswain.common.utils.constants import STATUS_ADDED


def getEnvironments(container: Container) -> List[Environment]:
    return Environment.select().where((Environment.container == container) & (Environment.status == STATUS_ADDED))


def cloneAll(from_container: Container, to_container: Container):
    for environment in getEnvironments(from_container):
        environment.id = None
        environment.container = to_container
        environment.save()


def deleteAll(container: Container):
    Environment.delete().where(Environment.container == container).execute()


def getEnvironment(env_id):
    return Environment.get(env_id)
