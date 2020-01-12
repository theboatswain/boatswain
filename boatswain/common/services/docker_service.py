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

import platform

import docker
from docker.models.containers import Container
from requests.exceptions import ConnectionError

from boatswain.common.exceptions.docker_exceptions import DockerNotAvailableException
from boatswain.common.services import global_preference_service
from boatswain.common.utils.constants import WINDOWS_BASE_URL, UNIX_BASE_URL
from boatswain.common.utils.logging import logger

system_platform = platform.system()
base_url = WINDOWS_BASE_URL if system_platform == "Windows" else UNIX_BASE_URL
client: docker.DockerClient


def setupClient():
    global client
    client = docker.DockerClient(base_url=global_preference_service.getCurrentDockerURL())


def searchDockerImages(keyword):
    ping()
    return client.images.search(keyword)


def getContainerInfo(container_id) -> Container:
    ping()
    return client.containers.get(container_id)


def inspect(container_id):
    ping()
    return docker.api.inspect_container(container_id)


def run(image_name, tag, ports, envs, volumes, entrypoint=None, **kwargs):
    ping()
    return client.containers.run(image_name + ":" + tag, detach=True, ports=ports,
                                 environment=envs, volumes=volumes, entrypoint=entrypoint, **kwargs)


def streamLogs(container_id: str):
    container = getContainerInfo(container_id)
    return container.logs(stream=True, timestamps=True)


def stop(container_id: str):
    ping()
    return client.containers.get(container_id)


def streamEvents():
    ping()
    return client.events(decode=True)


def ping():
    try:
        client.ping()
    except ConnectionError as e:
        raise DockerNotAvailableException()


def isDockerRunning():
    try:
        ping()
    except DockerNotAvailableException:
        logger.warning('Could not start boatswain because of the docker is not running')
        return False
    else:
        return True


def deleteContainer(container_id: str, delete_volumes=True):
    container = client.containers.get(container_id)
    container.remove(v=delete_volumes)


def deleteVolume(volume_id):
    client.volumes.get(volume_id).remove()
