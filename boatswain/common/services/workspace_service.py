from peewee import DoesNotExist

from boatswain.common.models.workspace import Workspace
from boatswain.common.services import global_preference_service
from boatswain.common.utils.constants import CURRENT_ACTIVATED_WORKSPACE


def getDefaultWorkspace():
    try:
        return Workspace.get(Workspace.name == 'Default')
    except DoesNotExist:
        workspace = Workspace(name='Default')
        workspace.save()
        return workspace


def getCurrentActivatedWorkspace():
    try:
        preference = global_preference_service.getPreference(CURRENT_ACTIVATED_WORKSPACE)
        workspace = Workspace.get(Workspace.id == preference.value)
    except DoesNotExist:
        workspace = getDefaultWorkspace()
        global_preference_service.setPreference(CURRENT_ACTIVATED_WORKSPACE, workspace.id)
    return workspace
