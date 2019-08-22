from PyQt5.QtCore import QSize
from peewee import DoesNotExist

from boatswain.common.models.preference import Preference
from boatswain.common.services import system_service
from boatswain.common.utils.constants import HOME_WIDTH, HOME_HEIGHT


def getPreference(key):
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
    height = system_service.screen_height * 4 / 5
    width = height / 1.7
    return QSize(width, height)


def getHomeWindowSize():
    try:
        preference_width = Preference.get(Preference.name == HOME_WIDTH)
        width = preference_width.value
        preference_height = Preference.get(Preference.name == HOME_HEIGHT)
        return QSize(int(width), int(preference_height.value))
    except DoesNotExist:
        return getMinimumHomeWindowSize()
