import logging
import os

from docker.errors import NotFound, DockerException

from common.models.container import Container
from common.models.environment import Environment
from common.models.port_mapping import PortMapping
from common.models.volume_mount import VolumeMount
from common.search.dockerhub_searcher import DockerHubSearcher
from common.search.search_images import SearchImages
from common.services import docker_service, config_service
from common.utils.constants import INCLUDING_ENV_SYSTEM, CONTAINER_CONF_CHANGED

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
            port.container = container;
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
    else:
        container_envs = {}

        if config_service.isAppConf(container, INCLUDING_ENV_SYSTEM, 'true'):
            for item in os.environ:
                if item != 'PATH':
                    container_envs[item] = os.environ[item]

        for environment in Environment.select().where(Environment.container == container):
            container_envs[environment.name] = environment.value

        ports = {}
        for port in PortMapping.select().where(PortMapping.container == container):
            ports[str(port.port) + '/' + port.protocol] = port.target_port

        volumes = {}
        for volume in VolumeMount.select():
            volumes[volume.host_path] = {'bind': volume.container_path, 'mode': volume.mode}

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
        logger.error("Exception occurred when trying to stop container", e)
    return False


def isInstanceOf(container: Container, dockerId):
    """
    Check if the given container and dockerId hash tag is from the same Container
    :param container: Container
    :param dockerId: hash tag ID of a container
    :return:
    """
    if container.container_id == '':
        return False
    return dockerId.startswith(container.container_id)

