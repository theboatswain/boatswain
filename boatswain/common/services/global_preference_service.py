from PyQt5.QtCore import QSize
from peewee import DoesNotExist

from boatswain.common.models.preference import Preference
from boatswain.common.utils.constants import HOME_WIDTH, HOME_HEIGHT


def setHomeWindowSize(size: QSize):
    try:
        preference_width = Preference.get(Preference.name == HOME_WIDTH)
        preference_width.value = size.width()
    except DoesNotExist:
        preference_width = Preference(name=HOME_WIDTH, value=size.width())
    preference_width.save()
    try:
        preference_height = Preference.get(Preference.name == HOME_HEIGHT)
        preference_height.value = size.height()
    except DoesNotExist:
        preference_height = Preference(name=HOME_HEIGHT, value=size.height())
    preference_height.save()


def getMinimumHomeWindowSize():
    return QSize(460, 639)


def getHomeWindowSize():
    try:
        preference_width = Preference.get(Preference.name == HOME_WIDTH)
        width = preference_width.value
        preference_height = Preference.get(Preference.name == HOME_HEIGHT)
        return QSize(int(width), int(preference_height.value))
    except DoesNotExist:
        return getMinimumHomeWindowSize()
