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

from boatswain.common.models.group import Group
from boatswain.common.services import workspace_service, global_preference_service
from boatswain.common.utils.constants import CURRENT_ACTIVATED_GROUP


def getDefaultGroup():
    workspace = workspace_service.getCurrentActivatedWorkspace()
    return getDefaultGroupFromWorkspace(workspace)


def getDefaultGroupFromWorkspace(workspace):
    try:
        return Group.get((Group.name == 'Default') & (Group.workspace == workspace))
    except DoesNotExist:
        group = Group(name='Default', workspace=workspace)
        group.save()
        return group


def getCurrentActivatedGroup():
    try:
        preference = global_preference_service.getPreference(CURRENT_ACTIVATED_GROUP)
        workspace = workspace_service.getCurrentActivatedWorkspace()
        group = Group.get((Group.name == preference.value) & (Group.workspace == workspace))
    except DoesNotExist:
        group = getDefaultGroup()
        activeGroup(group.name)
    return group


def activeGroup(name):
    global_preference_service.setPreference(CURRENT_ACTIVATED_GROUP, name)


def getGroups():
    return Group.select()


def createGroup(name):
    group = Group(name=name, workspace=workspace_service.getCurrentActivatedWorkspace())
    group.save()
    return group
