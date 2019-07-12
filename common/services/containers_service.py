import logging

from docker.errors import NotFound, DockerException

from common.models.container import Container
from common.models.environment import Environment
from common.models.port_mapping import PortMapping
from common.search.dockerhub_searcher import DockerHubSearcher
from common.search.search_images import SearchImages
from common.services import docker_service

logger = logging.getLogger(__name__)

# Initialising search engines
search_engine = SearchImages()
search_engine.addSearchProvider(DockerHubSearcher())


def installContainer(image_name, repo='dockerhub', description='', tag='latest', environments=None, ports=None):
    container = Container(image_name=image_name, description=description, tag=tag, name=image_name)
    container.save()

    if environments is not None:
        for env in environments:
            env.container = container
            env.save()
    if ports is not None:
        for port in ports:
            port.container = container;
            port.save()

    tags = search_engine.searchTags(image_name, repo)
    for tag in tags:
        tag.container = container
        tag.save()
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
    if isContainerExists(container):
        docker_container = docker_service.getContainerInfo(container.container_id)
        docker_container.start()
        return container
    else:
        container_envs = []
        for environment in Environment.select():
            if environment.container == container:
                container_envs.append(environment.name + '=' + environment.value)

        ports = {}
        for port in PortMapping.select():
            if port.container == container:
                ports[str(port.port) + '/' + port.protocol] = port.targetPort

        docker_container = docker_service.run(container, ports, container_envs)
        container.container_id = docker_container.short_id
        return container


def stopContainer(container: Container):
    try:
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
