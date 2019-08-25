from peewee import DoesNotExist

from boatswain.common.models.group import Group
from boatswain.common.services import workspace_service, global_preference_service
from boatswain.common.utils.constants import CURRENT_ACTIVATED_GROUP


def getDefaultGroup():
    try:
        workspace = workspace_service.getCurrentActivatedWorkspace()
        return Group.get((Group.name == 'Default') & (Group.workspace == workspace))
    except DoesNotExist:
        workspace = workspace_service.getCurrentActivatedWorkspace()
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
