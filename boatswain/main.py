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
import os
import sys

import docker
import requests
import platform
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox

from boatswain.common.models.configurations import Configuration
from boatswain.common.models.tag import Tag
from boatswain.common.services import boatswain_daemon, data_transporter_service
from boatswain.home.home import Home
from boatswain.common.models.base import db
from boatswain.common.models.container import Container
from boatswain.common.models.environment import Environment
from boatswain.common.models.port_mapping import PortMapping
from boatswain.common.models.volume_mount import VolumeMount
from boatswain.common.utils.logging import logger

from boatswain.common.utils.constants import APP_DATA_DIR, CONTAINER_CHANNEL, APP_EXIT_CHANNEL, WINDOWS_BASE_URL, \
    UNIX_BASE_URL


def show_warning_box():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Please make sure that docker is running")
    msg.exec()


def is_docker_running():
    system_platform = platform.system()
    base_url = WINDOWS_BASE_URL if system_platform == "Windows" else UNIX_BASE_URL
    client = docker.DockerClient(base_url=base_url)
    try:
        client.ping()
    except requests.exceptions.ConnectionError:
        logger.warning('Could not start boatswain because of the docker is not running')
        return False
    else:
        return True


def deFrostPem():
    """
    When the application is being frozen, all resource files will be encode into an executable file
    And with the requests library, it required to have the cacert.pem file available and accessible as a normal file
    thus caused the problem of invalid path: :/certifi/cacert.pem
    This function will workaround the problem by read the content of the pem file and write it into app data folder
    and then relink back the location of REQUESTS_CA_BUNDLE into this file
    """
    if not os.path.isfile(PEM_FILE):
        with closing(QFile(':/certifi/cacert.pem')) as pem_file:
            if pem_file.open(QFile.ReadOnly):
                pem_data = bytes(pem_file.readAll()).decode('UTF-8')
                with open(PEM_FILE, 'w') as the_file:
                    the_file.write(pem_data)

    if os.path.isfile(PEM_FILE):
        os.environ['REQUESTS_CA_BUNDLE'] = PEM_FILE


def main():
    app = QApplication(sys.argv)
    if is_docker_running():

        # Make sure app data dir always exists
        if not os.path.isdir(APP_DATA_DIR):
            os.makedirs(APP_DATA_DIR)

        logger.info("App data path: %s" % APP_DATA_DIR)
    deFrostPem()

        # Connect to SQLite DB
        db.connect()
        db.create_tables([Container, Environment, PortMapping, VolumeMount, Tag, Configuration])

        # Load home window
        window = Home()

        # Load all installed containers
        for container in Container.select():
            data_transporter_service.fire(CONTAINER_CHANNEL, container)

        # Close db before exit
        data_transporter_service.listen(APP_EXIT_CHANNEL, lambda x: db.close())

        daemon = boatswain_daemon.BoatswainDaemon(window)
        daemon.start()

        # Stop daemon before exit
        data_transporter_service.listen(APP_EXIT_CHANNEL, lambda x: daemon.events.close())
        sys.exit(app.exec_())
    else:
        show_warning_box()


if __name__ == '__main__':
    main()
