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

from PyQt5.QtCore import QSize
from peewee import DoesNotExist

from boatswain.common.models.preference import Preference
from boatswain.common.services import system_service
from boatswain.common.utils.constants import HOME_WIDTH, HOME_HEIGHT


def getPreference(key) -> Preference:
    return Preference.get(Preference.name == key)


def setPreference(key, value):
    try:
        preference = getPreference(key)
        preference.value = value
    except DoesNotExist:
        preference = Preference(name=key, value=value)
    preference.save()


def setHomeWindowSize(size: QSize):
    setPreference(HOME_WIDTH, size.width())
    setPreference(HOME_HEIGHT, size.height())


def getMinimumHomeWindowSize():
    height = system_service.screen_height * 4.2 / 5
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
