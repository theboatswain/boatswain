from peewee import DoesNotExist

from boatswain.common.models.group import Group
from boatswain.common.services import workspace_service


def getDefaultGroup():
    try:
        return Group.get(Group.name == 'Default')
    except DoesNotExist:
        workspace = workspace_service.getCurrentActivatedWorkspace()
        group = Group(name='Default', workspace=workspace)
        group.save()
        return group
