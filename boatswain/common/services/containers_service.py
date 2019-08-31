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

import logging
import os
from typing import List

from docker.errors import NotFound

from boatswain.common.models.container import Container
from boatswain.common.models.workspace import Workspace
from boatswain.common.search.dockerhub_searcher import DockerHubSearcher
from boatswain.common.search.search_images import SearchImages
from boatswain.common.services import docker_service, system_service, config_service, data_transporter_service, \
    shortcut_service, group_service, environment_service, port_mapping_service, volume_mount_service, tags_service
from boatswain.common.utils import docker_utils
from boatswain.common.utils.constants import INCLUDING_ENV_SYSTEM, CONTAINER_CONF_CHANGED, \
    CONTAINER_CONF_CHANGED_CHANNEL

logger = logging.getLogger(__name__)

# Initialising search engines
search_engine = SearchImages()
search_engine.addSearchProvider(DockerHubSearcher())


def updateContainerTags(container: Container):
    tags = search_engine.searchTags(container.image_name, container.repo)
    for tag in tags:
        tag.container = container
        tag.save()


def getContainer(container_id: int) -> Container:
    return Container.get(Container.id == container_id)


def getAllContainer() -> List[Container]:
    return Container.select().order_by(Container.order.asc())


def getNextOrder(container: Container):
    try:
        next_container = Container.select()\
            .where(Container.order > container.order)\
            .order_by(Container.order.asc())\
            .first()
        return round((next_container.order + container.order) / 2)
    except AttributeError:
        return container.order + 10000


def installContainer(image_name, repo='dockerhub', description='', tag='latest', environments=None, ports=None,
                     group=None):
    order = Container.select().count() * 10000
    if not group:
        group = group_service.getDefaultGroup()
    container = Container(image_name=image_name, description=description, tag=tag, name=image_name,
                          repo=repo, group=group, order=order)
    container.save()

    if environments is not None:
        for env in environments:
            env.container = container
            env.save()
    if ports is not None:
        for port in ports:
            port.container = container
            port.save()

    updateContainerTags(container)
    return container


def isAppInstalled(image_name):
    for container in Container.select():
        if container.image_name == image_name:
            return True
    return False


def searchImages(keyword, repo_filter):
    return search_engine.search(keyword, repo_filter)


def isContainerExists(container: Container):
    try:
        if container.container_id != "":
            docker_service.getContainerInfo(container.container_id)
            return True
    except NotFound:
        if container.container_id != "":
            container.container_id = ""
            container.save()
    return False


def isContainerRunning(container: Container):
    """
    Check whether or not the given container is running or not
    :param container:
    :return:
    """
    if isContainerExists(container):
        container_info = docker_service.getContainerInfo(container.container_id)
        return container_info.status == "running"
    return False


def startContainer(container: Container):
    """
    Start the given container
    Collecting all configurations of the given container including environments, port mapping, volume mounts and
    shortcuts. The preferences of Shortcut take highest priority and will override if it existing in
    any other configurations
    :param container: container to be start
    :return: assign the container id and return container object
    """
    if config_service.isAppConf(container, CONTAINER_CONF_CHANGED, 'true'):
        container.container_id = ""
        container.save()
        config_service.setAppConf(container, CONTAINER_CONF_CHANGED, 'false')
        # Todo: Should we do the clean up? delete the downloaded image

    if isContainerExists(container):
        docker_container = docker_service.getContainerInfo(container.container_id)
        docker_container.start()
        return container

    container_envs = {}

    if config_service.isAppConf(container, INCLUDING_ENV_SYSTEM, 'true'):
        container_envs = {key: os.environ[key] for key in os.environ if key != 'PATH'}

    for environment in environment_service.getEnvironments(container):
        container_envs[environment.name] = environment.value

    container_envs = {**container_envs, **shortcut_service.getShortcutContainerEnvs(container)}

    ports = {}
    for port in port_mapping_service.getPortMappings(container):
        ports[str(port.port) + '/' + port.protocol] = port.target_port

    ports = {**ports, **shortcut_service.getShortcutPortMapping(container)}

    volumes = {}
    for volume in volume_mount_service.getVolumeMounts(container):
        volumes[volume.host_path] = {'bind': volume.container_path, 'mode': volume.mode}

    volumes = {**volumes, **shortcut_service.getShortcutVolumeMounts(container)}

    docker_container = docker_service.run(container, ports, container_envs, volumes)
    container.container_id = docker_container.short_id
    return container


def stopContainer(container: Container):
    if isContainerRunning(container):
        docker_container = docker_service.stop(container)
        docker_container.stop(timeout=20)
    return True


def cloneContainer(container: Container, workspace: Workspace):
    """
    Duplicate Container from one workspace to the other. Destination can be the same workspace
    :param container: container to be duplicate
    :param workspace: workspace destination
    :return: the cloned version of container
    """
    group_dest = group_service.getDefaultGroupFromWorkspace(workspace)
    clone = Container.get(Container.id == container.id)
    clone.group = group_dest
    clone.container_id = ''
    clone.name = container.name + ' - cloned'
    clone.id = None
    clone.save()
    shortcut_service.cloneAll(container, clone)
    environment_service.cloneAll(container, clone)
    port_mapping_service.cloneAll(container, clone)
    volume_mount_service.cloneAll(container, clone)
    tags_service.cloneAll(container, clone)
    config_service.cloneAll(container, clone)
    return clone


def deleteConfigurations(container: Container):
    stopContainer(container)
    config_service.deleteAll(container)
    environment_service.deleteAll(container)
    port_mapping_service.deleteAll(container)
    shortcut_service.deleteAll(container)
    volume_mount_service.deleteAll(container)


def deleteContainer(container: Container):
    """
    Delete the instance of the given container as well as all of it's configurations
    :param container: Container
    """
    deleteConfigurations(container)
    tags_service.deleteAll(container)
    container.delete_instance()


def isInstanceOf(container: Container, docker_id):
    """
    Check if the given container and dockerId hash tag is from the same Container
    :param container: Container
    :param docker_id: hash tag ID of a container
    :return:
    """
    if container.container_id == '':
        return False
    return docker_id.startswith(container.container_id)


def connectToContainer(container):
    if isContainerRunning(container):
        command = ['docker', 'exec', '-ti', container.container_id, '/bin/sh']
        system_service.startTerminalWithCommand(' '.join(command))
    else:
        message = 'Container have to be running before connecting to it\'s shell'
        docker_utils.notifyContainerNotRunning(container, message)


def listen(container: Container, name, func):
    key = CONTAINER_CONF_CHANGED_CHANNEL + '_' + str(container.id) + '_' + name
    data_transporter_service.listen(key, func)


def fire(container: Container, name, value):
    key = CONTAINER_CONF_CHANGED_CHANNEL + '_' + str(container.id) + '_' + name
    data_transporter_service.fire(key, value)
