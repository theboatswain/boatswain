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

from boatswain.common.models.group import Group
from boatswain.common.models.workspace import Workspace
from boatswain.common.services import workspace_service


def getDefaultGroup():
    workspace = workspace_service.getCurrentActivatedWorkspace()
    return getDefaultGroupFromWorkspace(workspace)


def getDefaultGroupFromWorkspace(workspace):
    try:
        return Group.get(Group.is_default & (Group.workspace == workspace))
    except DoesNotExist:
        return createGroupFromWorkspace('Default', workspace, is_default=True)


def getGroups():
    return Group.select().order_by(Group.order.asc())


def createGroup(name):
    return createGroupFromWorkspace(name, workspace_service.getCurrentActivatedWorkspace())


def createGroupFromWorkspace(name, workspace: Workspace, is_default=False):
    order = Group.select().count() * 10000
    group = Group(name=name, workspace=workspace, order=order, is_default=is_default)
    group.save()
    return group


def getNextOrder(group: Group):
    try:
        next_group = Group.select() \
            .where(Group.order > group.order) \
            .order_by(Group.order.asc()) \
            .first()
        return round((next_group.order + group.order) / 2)
    except AttributeError:
        return group.order + 10000


def getGroup(group_id: int) -> Group:
    return Group.get(Group.id == group_id)


def deleteGroup(group: Group):
    group.delete_instance()
