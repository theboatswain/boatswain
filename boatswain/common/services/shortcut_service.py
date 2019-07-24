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
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#
from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut


def getShortcutContainerEnvs(container: Container):
    """
    Get all shortcut environment variables that link with the given container
    :return: Dict: {'<key>': '<value>'}
    """
    result = {}
    shortcuts = PreferencesShortcut.select().where(
        (PreferencesShortcut.container == container) & (PreferencesShortcut.shortcut == 'Environment'))
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
    shortcuts = PreferencesShortcut.select().where(
        (PreferencesShortcut.container == container) & (PreferencesShortcut.shortcut == 'Port Mapping'))
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
    :rtype: 
    """
    result = {}
    shortcuts = PreferencesShortcut.select().where(
        (PreferencesShortcut.container == container) & (PreferencesShortcut.shortcut == 'Volume Mount'))
    for item in shortcuts:
        result[item.default_value] = {'bind': item.mapping_to, 'mode': 'rw'}
    return result

