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
import os
from typing import List

from peewee import DoesNotExist
from playhouse.shortcuts import update_model_from_dict

from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.utils.logging import logger


def getShortcutContainerEnvs(container: Container):
    """
    Get all shortcut environment variables that link with the given container
    :return: Dict: {'<key>': '<value>'}
    """
    result = {}
    shortcuts = PreferencesShortcut.select().where((PreferencesShortcut.container == container)
                                                   & (PreferencesShortcut.shortcut == 'Environment')
                                                   & PreferencesShortcut.enabled)
    for item in shortcuts:
        result[item.mapping_to] = item.default_value
    return result


def getShortcutPortMapping(container: Container):
    """
    Get all shortcut port mapping that link with the given container

    :return: Dict: {'<container port>/tcp': <host port>}
    :rtype:
    """
    result = {}
    shortcuts = PreferencesShortcut.select().where((PreferencesShortcut.container == container)
                                                   & (PreferencesShortcut.shortcut == 'Port Mapping')
                                                   & PreferencesShortcut.enabled)
    for item in shortcuts:
        result[item.mapping_to + '/tcp'] = item.default_value
    return result


def getShortcutVolumeMounts(container: Container):
    """
    Get all shortcut volume mounts that linked with the given container

    :return: Dict: {'<host path>': {
                        'bind': '<container path>'
                        'mode': 'rw'}
                    }
    """
    result = {}
    shortcuts = PreferencesShortcut.select().where((PreferencesShortcut.container == container)
                                                   & (PreferencesShortcut.shortcut == 'Volume Mount')
                                                   & PreferencesShortcut.enabled)
    for item in shortcuts:
        result[item.default_value] = {'bind': item.mapping_to, 'mode': 'rw'}
    return result


def getShortcuts(container: Container) -> List[PreferencesShortcut]:
    return PreferencesShortcut.select().where(PreferencesShortcut.container == container)\
        .order_by(PreferencesShortcut.order.asc())


def getEnabledShortcuts(container: Container) -> List[PreferencesShortcut]:
    return PreferencesShortcut.select().where(
        (PreferencesShortcut.container == container) & PreferencesShortcut.enabled) \
        .order_by(PreferencesShortcut.order.asc())


def cloneAll(from_container: Container, to_container: Container):
    for shortcut in getShortcuts(from_container):
        shortcut.id = None
        shortcut.container = to_container
        shortcut.save()


def deleteAll(container: Container):
    PreferencesShortcut.delete().where(PreferencesShortcut.container == container).execute()


def importShortcuts(container: Container, shortcuts: List[dict]):
    for shortcut_dict in shortcuts:
        shortcut = PreferencesShortcut()
        update_model_from_dict(shortcut, shortcut_dict)
        shortcut.container = container
        if shortcut.pref_type in ['File', 'Folder']:
            if not os.path.exists(shortcut.default_value):
                shortcut.default_value = ''
        try:
            PreferencesShortcut.get((PreferencesShortcut.container == container)
                                    & (PreferencesShortcut.shortcut == shortcut.shortcut)
                                    & (PreferencesShortcut.mapping_to == shortcut.mapping_to)
                                    & (PreferencesShortcut.pref_type == shortcut.pref_type))
            logger.info("Ignoring shortcut label %s cuz it is already exists" % shortcut.label)
        except DoesNotExist:
            shortcut.save()
