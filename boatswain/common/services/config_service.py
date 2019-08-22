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

from peewee import DoesNotExist

from boatswain.common.models.configurations import Configuration
from boatswain.common.models.container import Container
from boatswain.common.utils.constants import APP_EXPANDED


def getAppConf(container: Container, key: str) -> Configuration:
    return Configuration.get(Configuration.container == container, Configuration.name == key)


def isAppConf(container: Container, key: str, value: str) -> bool:
    try:
        conf = getAppConf(container, key)
        return conf.value == value
    except DoesNotExist:
        return False


def setAppConf(container: Container, key: str, value: str):
    try:
        conf = getAppConf(container, key)
        conf.value = value
        conf.save()
    except DoesNotExist:
        Configuration.create(container=container, name=key, value=value)


def isAppExpanded(container: Container):
    return isAppConf(container, APP_EXPANDED, 'true')


def setAppExpanded(container: Container, expand: bool):
    if expand:
        setAppConf(container, APP_EXPANDED, 'true')
    else:
        setAppConf(container, APP_EXPANDED, 'false')
