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
    return Workspace.select()


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
