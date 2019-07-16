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
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox

from common.models.base import db
from common.models.configurations import Configuration
from common.models.container import Container
from common.models.environment import Environment
from common.models.port_mapping import PortMapping
from common.models.tag import Tag
from common.models.volume_mount import VolumeMount
from common.services import data_transporter_service, boatswain_daemon
from common.utils.constants import APP_DATA_DIR, CONTAINER_CHANNEL, APP_EXIT_CHANNEL
from common.utils.logging import logger
from home.home import Home


def set_app_icon():
    app_icon = QIcon()
    app_icon.addFile('home/icon/boatswain-16x16.png', QSize(16, 16))
    app_icon.addFile('home/icon/boatswain-24x24.png', QSize(24, 24))
    app_icon.addFile('home/icon/boatswain-32x32.png', QSize(32, 32))
    app_icon.addFile('home/icon/boatswain-48x48.png', QSize(48, 48))
    app_icon.addFile('home/icon/boatswain-256x256.png', QSize(256, 256))
    app.setWindowIcon(app_icon)


def show_warning_box():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Please make sure that docker is running")
    msg.exec()


def is_docker_running():
    client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    try:
        client.ping()
    except requests.exceptions.ConnectionError:
        logger.warn('Could not start boatswain because of the docker is not running')
        return False
    else:
        return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    if is_docker_running():

        # Make sure app data dir always exists
        if not os.path.isdir(APP_DATA_DIR):
            os.makedirs(APP_DATA_DIR)

        logger.info("App data path: %s" % APP_DATA_DIR)

        # Connect to SQLite DB
        db.connect()
        db.create_tables([Container, Environment, PortMapping, VolumeMount, Tag, Configuration])

        # Set default icon
        set_app_icon()

        # Load home window
        window = Home()

        # Load all installed containers
        for container in Container.select():
            data_transporter_service.fire(CONTAINER_CHANNEL, container)

        # Close db before exit
        data_transporter_service.listen(APP_EXIT_CHANNEL, lambda x: db.close())

        daemon = boatswain_daemon.BoatswainDaemon(window)
        daemon.__init__()
        daemon.start()

        # Stop daemon before exit
        data_transporter_service.listen(APP_EXIT_CHANNEL, lambda x: daemon.events.close())
        sys.exit(app.exec_())
    else:
        show_warning_box()