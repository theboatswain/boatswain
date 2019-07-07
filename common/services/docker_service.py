import docker

from common.models.container import Container

client = docker.DockerClient(base_url='unix://var/run/docker.sock')


def searchDockerhubContainers(keyword):
    return client.images.search(keyword)


def getContainerInfo(container_id):
    return client.containers.get(container_id)


def run(container: Container, ports, envs):
    return client.containers.run(container.image_name + ":" + container.tag,
                                 detach=True, ports=ports, environment=envs)


def stop(container: Container):
    return client.containers.get(container.container_id)
