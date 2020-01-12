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

from peewee import DoesNotExist

from boatswain.common.exceptions.workspace import WorkspaceAlreadyExistsException
from boatswain.common.models.workspace import Workspace
from boatswain.common.services import global_preference_service
from boatswain.common.utils.constants import CURRENT_ACTIVATED_WORKSPACE


def getDefaultWorkspace():
    try:
        return Workspace.get(Workspace.name == 'All')
    except DoesNotExist:
        workspace = Workspace(name='All')
        workspace.save()
        return workspace


def getCurrentActivatedWorkspace():
    try:
        preference = global_preference_service.getPreference(CURRENT_ACTIVATED_WORKSPACE)
        workspace = Workspace.get(Workspace.name == preference.value)
    except DoesNotExist:
        workspace = getDefaultWorkspace()
        activeWorkspace(workspace.name)
    return workspace


def activeWorkspace(workspace):
    global_preference_service.setPreference(CURRENT_ACTIVATED_WORKSPACE, workspace)


def getWorkspaces():
    return Workspace.select().where(Workspace.name != 'All')


def getWorkspace(name):
    return Workspace.get(Workspace.name == name)


def createWorkspace(name):
    try:
        Workspace.get(Workspace.name == name)
        raise WorkspaceAlreadyExistsException()
    except DoesNotExist:
        workspace = Workspace(name=name)
        workspace.save()
        return workspace
