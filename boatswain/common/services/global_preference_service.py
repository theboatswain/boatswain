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

from PyQt5.QtCore import QSize, Qt
from boatswain_updater.utils import sys_utils
from peewee import DoesNotExist

from boatswain.common.models.preference import Preference
from boatswain.common.services import system_service
from boatswain.common.utils.constants import HOME_WIDTH, HOME_HEIGHT, PROTOCOL_KEY, AUTOMATIC_UPDATE

in_memory_variables = {}


def getPreference(key) -> Preference:
    return Preference.get(Preference.name == key)


def getInMemoryPreferences(key):
    if key in in_memory_variables:
        return in_memory_variables[key]
    return None


def setInMemoryPreferences(key, value):
    in_memory_variables[key] = value


def getPreferenceValue(key, default=None) -> str:
    try:
        preference = getPreference(key)
        return preference.value
    except DoesNotExist:
        return default


def setPreference(key, value):
    try:
        preference = getPreference(key)
        preference.value = value
    except DoesNotExist:
        preference = Preference(name=key, value=value)
    preference.save()


def isAutomaticUpdate():
    try:
        preference = getPreference(AUTOMATIC_UPDATE)
        return preference.value == str(Qt.Checked)
    except DoesNotExist:
        return True


def removePreference(key):
    try:
        preference = getPreference(key)
        preference.delete_instance()
    except DoesNotExist:
        pass


def getCurrentDockerURL():
    try:
        return getPreference(PROTOCOL_KEY).value
    except DoesNotExist:
        if sys_utils.isWin():
            return 'tcp://127.0.0.1:2375'
        else:
            return 'unix://var/run/docker.sock'


def setHomeWindowSize(size: QSize):
    setPreference(HOME_WIDTH, size.width())
    setPreference(HOME_HEIGHT, size.height())


def getMinimumHomeWindowSize():
    height = system_service.getRefHeight() * 4.2 / 5
    width = height / 1.8
    return QSize(width, height)


def getHomeWindowSize():
    try:
        preference_width = Preference.get(Preference.name == HOME_WIDTH)
        width = preference_width.value
        preference_height = Preference.get(Preference.name == HOME_HEIGHT)
        return QSize(int(width), int(preference_height.value))
    except DoesNotExist:
        return getMinimumHomeWindowSize()
