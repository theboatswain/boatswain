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
