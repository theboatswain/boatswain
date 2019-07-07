import logging

from docker.errors import NotFound, ContainerError, APIError

from common.models.container import Container
from common.models.environment import Environment
from common.models.port_mapping import PortMapping
from common.search.dockerhub_searcher import DockerHubSearcher
from common.search.search_images import SearchImages

# Initialising search engines
from common.services import docker_service

logger = logging.getLogger(__name__)

search_engine = SearchImages()
search_engine.addSearchProvider(DockerHubSearcher())


def installContainer(image_name, repo='dockerhub', description='', tag='latest', environments=None, ports=None):
    container = Container(image_name=image_name, description=description, tag=tag, status='INSTALLED')
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
    except NotFound as e:
        logger.error("Exception occurred. Container should be there. ", e)
        container.container_id = ""
        container.save()
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
    except ContainerError:
        print("got ContainerError error")
    except APIError:
        print('got APIError error')
