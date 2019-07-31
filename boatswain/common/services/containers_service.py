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

from docker.errors import NotFound, DockerException

from boatswain.common.models.configurations import Configuration
from boatswain.common.models.container import Container
from boatswain.common.models.environment import Environment
from boatswain.common.models.port_mapping import PortMapping
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.models.tag import Tag
from boatswain.common.models.volume_mount import VolumeMount
from boatswain.common.search.dockerhub_searcher import DockerHubSearcher
from boatswain.common.search.search_images import SearchImages
from boatswain.common.services import docker_service, system_service, config_service, data_transporter_service, \
    shortcut_service
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


def installContainer(image_name, repo='dockerhub', description='', tag='latest', environments=None, ports=None):
    container = Container(image_name=image_name, description=description, tag=tag, name=image_name, repo=repo)
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
    # Todo: Should we do this? [Performance]
    # Yes, we should, let's do it by checking image name and registry url
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
    if isContainerExists(container):
        container_info = docker_service.getContainerInfo(container.container_id)
        return container_info.status == "running"
    return False


def startContainer(container: Container):
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

    for environment in Environment.select().where(Environment.container == container):
        container_envs[environment.name] = environment.value

    container_envs = {**container_envs, **shortcut_service.getShortcutContainerEnvs(container)}

    ports = {}
    for port in PortMapping.select().where(PortMapping.container == container):
        ports[str(port.port) + '/' + port.protocol] = port.target_port

    ports = {**ports, **shortcut_service.getShortcutPortMapping(container)}

    volumes = {}
    for volume in VolumeMount.select().where(VolumeMount.container == container):
        volumes[volume.host_path] = {'bind': volume.container_path, 'mode': volume.mode}

    volumes = {**volumes, **shortcut_service.getShortcutVolumeMounts(container)}

    docker_container = docker_service.run(container, ports, container_envs, volumes)
    container.container_id = docker_container.short_id
    return container


def stopContainer(container: Container):
    try:
        if isContainerRunning(container):
            docker_container = docker_service.stop(container)
            docker_container.stop(timeout=20)
        return True
    except DockerException as e:
        logger.error("Exception occurred when trying to stop container, %s", e)
    return False


def deleteConfigurations(container: Container):
    stopContainer(container)
    Configuration.delete().where(Configuration.container == container).execute()
    Environment.delete().where(Environment.container == container).execute()
    PortMapping.delete().where(PortMapping.container == container).execute()
    PreferencesShortcut.delete().where(PreferencesShortcut.container == container).execute()
    VolumeMount.delete().where(VolumeMount.container == container).execute()


def deleteContainer(container: Container):
    deleteConfigurations(container)
    Tag.delete().where(Tag.container == container).execute()
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
