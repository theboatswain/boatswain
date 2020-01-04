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

import os
import sys

from PyQt5.QtCore import Qt, QCoreApplication, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from boatswain_updater.models.feed import Feed
from boatswain_updater.updater import Updater

from boatswain.common.models.base import db
from boatswain.common.models.tables import db_tables
from boatswain.common.services import boatswain_daemon, data_transporter_service, docker_service, system_service, \
    containers_service
from boatswain.common.utils import docker_utils
from boatswain.common.utils.constants import APP_DATA_DIR, APP_EXIT_CHANNEL, UPDATES_CHANNEL, APP_AVATAR_DIR
from boatswain.common.utils.logging import logger
from boatswain.home.home import Home
from boatswain.resources_utils import getExternalResource


def onApplicationInstalled():
    # Once the application is updated, then relaunch it self
    data_transporter_service.fire(APP_EXIT_CHANNEL)
    logger.info('Relaunching %s' % sys.executable)
    os.execlp(sys.executable, *sys.argv)


def run():
    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    QCoreApplication.setApplicationVersion("0.0.0")
    QCoreApplication.setApplicationName("Boatswain")
    app = QApplication(sys.argv)
    system_service.resetStyle()
    system_service.initialisingPath()

    if not docker_service.isDockerRunning():
        return docker_utils.notifyDockerNotAvailable()

    # Make sure app data dir always exists
    if not os.path.isdir(APP_DATA_DIR):
        os.makedirs(APP_DATA_DIR)
    if not os.path.isdir(APP_AVATAR_DIR):
        os.makedirs(APP_AVATAR_DIR)

    system_service.reassignPemLocation()
    logger.info("App data path: %s", APP_DATA_DIR)

    # Connect to SQLite DB
    db.connect()
    db.create_tables(db_tables)

    # Load home window
    window = Home()

    # Close db before exit
    data_transporter_service.listen(APP_EXIT_CHANNEL, lambda: db.close())

    # Create daemon to listen to docker events
    daemon = boatswain_daemon.BoatswainDaemon(window.ui)
    daemon.start()

    feed = Feed('theboatswain/boatswain')
    pixmap = QIcon(getExternalResource('boatswain.svg')).pixmap(QSize(64, 64))
    update_dialog = Updater(None, feed)
    update_dialog.setIcon(pixmap)
    update_dialog.installed.connect(onApplicationInstalled)
    update_dialog.checkForUpdate(silent=True)
    data_transporter_service.listen(UPDATES_CHANNEL, update_dialog.checkForUpdate)

    window.show()

    # Prefetch default containers for search
    containers_service.prefetchDefaultContainersInBackground()

    # Stop daemon before exit
    data_transporter_service.listen(APP_EXIT_CHANNEL, lambda: daemon.events.close())
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
