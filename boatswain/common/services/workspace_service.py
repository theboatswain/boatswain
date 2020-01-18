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

from peewee import DoesNotExist

from boatswain.common.exceptions.workspace import WorkspaceAlreadyExistsException, WorkspaceIsNotEmptiedException
from boatswain.common.models.workspace import Workspace
from boatswain.common.services import global_preference_service, group_service
from boatswain.common.utils.constants import CURRENT_ACTIVATED_WORKSPACE


def getDefaultWorkspace() -> Workspace:
    try:
        return Workspace.get(Workspace.is_default)
    except DoesNotExist:
        workspace = Workspace(name='All', is_default=True)
        workspace.save()
        return workspace


def getCurrentActivatedWorkspace() -> Workspace:
    try:
        preference = global_preference_service.getPreference(CURRENT_ACTIVATED_WORKSPACE)
        workspace = Workspace.get(Workspace.id == int(preference.value))
    except (DoesNotExist, ValueError):
        workspace = getDefaultWorkspace()
        activeWorkspace(workspace.id)
    return workspace


def activeWorkspace(workspace_id: int):
    global_preference_service.setPreference(CURRENT_ACTIVATED_WORKSPACE, workspace_id)


def getWorkspaces() -> List[Workspace]:
    """
    Return list of workspaces, NOT including default one
    @return: array
    """
    return Workspace.select().where(Workspace.is_default == False).order_by(Workspace.name.asc())


def getWorkspace(name: str) -> Workspace:
    return Workspace.get(Workspace.name == name)


def isWorkspaceNameAvailable(name: str) -> bool:
    """
    Check if the given workspace name is available
    return True if it is, otherwise, False
    @param name: str
    @return: boolean
    """
    try:
        Workspace.get(Workspace.name == name)
        return False
    except DoesNotExist:
        return True


def getWorkspaceById(ws_id: int) -> Workspace:
    return Workspace.get(Workspace.id == ws_id)


def createWorkspace(name: int) -> Workspace:
    try:
        Workspace.get(Workspace.name == name)
        raise WorkspaceAlreadyExistsException()
    except DoesNotExist:
        workspace = Workspace(name=name)
        workspace.save()
        return workspace


def deleteWorkspace(workspace_id: int):
    """
    Delete a workspace and all of its groups and containers
    @param workspace_id: workspace id
    """
    workspace = Workspace.get(Workspace.id == workspace_id)
    groups = group_service.getGroupsFromWorkspace(workspace)
    if len(groups) == 0:
        workspace.delete_instance()
    else:
        raise WorkspaceIsNotEmptiedException()
