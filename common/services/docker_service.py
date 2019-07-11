import docker

from common.exceptions.docker_exceptions import DockerNotAvailableException
from common.models.container import Container
from requests.exceptions import ConnectionError

client = docker.DockerClient(base_url='unix://var/run/docker.sock')


def searchDockerhubContainers(keyword):
    ping()
    return client.images.search(keyword)


def getContainerInfo(container_id):
    ping()
    return client.containers.get(container_id)


def run(container: Container, ports, envs):
    ping()
    return client.containers.run(container.image_name + ":" + container.tag,
                                 detach=True, ports=ports, environment=envs)


def stop(container: Container):
    ping()
    return client.containers.get(container.container_id)


def ping():
    try:
        client.ping()
    except ConnectionError:
        raise DockerNotAvailableException()
