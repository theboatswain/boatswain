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
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#

import platform

import docker
from requests.exceptions import ConnectionError

from boatswain.common.exceptions.docker_exceptions import DockerNotAvailableException
from boatswain.common.models.container import Container
from boatswain.common.utils.constants import WINDOWS_BASE_URL, UNIX_BASE_URL
from boatswain.common.utils.logging import logger

system_platform = platform.system()
base_url = WINDOWS_BASE_URL if system_platform == "Windows" else UNIX_BASE_URL
client = docker.DockerClient(base_url=base_url)


def searchDockerhubContainers(keyword):
    ping()
    return client.images.search(keyword)


def getContainerInfo(container_id):
    ping()
    return client.containers.get(container_id)


def run(container: Container, ports, envs, volumes):
    ping()
    return client.containers.run(container.image_name + ":" + container.tag, detach=True, ports=ports,
                                 environment=envs, volumes=volumes)


def stop(container: Container):
    ping()
    return client.containers.get(container.container_id)


def streamEvents():
    ping()
    return client.events(decode=True)


def ping():
    try:
        client.ping()
    except ConnectionError:
        raise DockerNotAvailableException()


def isDockerRunning():
    try:
        ping()
    except DockerNotAvailableException:
        logger.warning('Could not start boatswain because of the docker is not running')
        return False
    else:
        return True
