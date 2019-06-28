import os
import sys

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from controllers.home.home import Home
from domains.base import db
from domains.container import Container
from domains.environment import Environment
from domains.port_mapping import PortMapping
from domains.volume_mount import VolumeMount
from services import data_transporter_service
from utils.constants import APP_DATA_DIR, CONTAINER_CHANNEL, APP_EXIT_CHANNEL

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Make sure app data dir always exists
    if not os.path.isdir(APP_DATA_DIR):
        os.makedirs(APP_DATA_DIR)

    # Connect to SQLite DB
    db.connect()
    db.create_tables([Container, Environment, PortMapping, VolumeMount])

    # Set default icon
    app_icon = QIcon()
    app_icon.addFile('resources/icon/boatswain-16x16.png', QSize(16, 16))
    app_icon.addFile('resources/icon/boatswain-24x24.png', QSize(24, 24))
    app_icon.addFile('resources/icon/boatswain-32x32.png', QSize(32, 32))
    app_icon.addFile('resources/icon/boatswain-48x48.png', QSize(48, 48))
    app_icon.addFile('resources/icon/boatswain-256x256.png', QSize(256, 256))
    app.setWindowIcon(app_icon)

    # Load home window
    window = Home()

    # Load all installed containers
    for container in Container.select():
        data_transporter_service.fire(CONTAINER_CHANNEL, container)

    # Close db before exit
    data_transporter_service.listen(APP_EXIT_CHANNEL, lambda x: db.close())
    sys.exit(app.exec_())
