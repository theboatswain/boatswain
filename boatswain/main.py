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
from boatswain.common.services import data_transporter_service, system_service, \
    containers_service, docker_service, style_service
from boatswain.common.utils import utils
from boatswain.common.utils.constants import APP_DATA_DIR, APP_EXIT_CHANNEL, UPDATES_CHANNEL, APP_AVATAR_DIR, \
    THEME_UPDATING_CHANNEL
from boatswain.common.utils.logging import logger
from boatswain.home.home import Home
from boatswain.resources_utils import getExternalResource

APP_VERSION = "1.1.0"


def onApplicationInstalled():
    # Once the application is updated, then relaunch it self
    data_transporter_service.fire(APP_EXIT_CHANNEL)
    logger.info('Relaunching %s' % sys.executable)
    os.execlp(sys.executable, *sys.argv)


def run():
    QApplication.setAttribute(Qt.AA_DisableHighDpiScaling)
    QCoreApplication.setApplicationVersion(APP_VERSION)
    QCoreApplication.setApplicationName("Boatswain")
    app = QApplication(sys.argv)
    system_service.resetStyle()
    system_service.initialisingPath()

    # Make sure app data dir always exists
    if not os.path.isdir(APP_DATA_DIR):
        os.makedirs(APP_DATA_DIR)
    if not os.path.isdir(APP_AVATAR_DIR):
        os.makedirs(APP_AVATAR_DIR)

    # Connect to SQLite DB
    # migration()
    db.connect(reuse_if_open=True)
    db.create_tables(db_tables)
    docker_service.setupClient()

    system_service.reassignPemLocation()
    logger.info("App data path: %s", APP_DATA_DIR)

    data_transporter_service.listen(THEME_UPDATING_CHANNEL, app.setStyleSheet)
    theme_path = style_service.getCurrentActivatedThemePath()
    style_service.activateTheme(theme_path)

    # Load home window
    window = Home()

    # Close db before exit
    data_transporter_service.listen(APP_EXIT_CHANNEL, lambda: db.close())

    feed = Feed('theboatswain/boatswain')
    pixmap = QIcon(getExternalResource('boatswain.svg')).pixmap(QSize(64, 64))
    update_dialog = Updater(None, feed)
    update_dialog.setIcon(pixmap)
    update_dialog.installed.connect(onApplicationInstalled)
    style_service.optimiseUpdaterUi(update_dialog)
    # update_dialog.checkForUpdate(silent=True)
    data_transporter_service.listen(UPDATES_CHANNEL, update_dialog.checkForUpdate)

    if docker_service.isDockerRunning():
        window.show()
    else:
        # At this point, if the docker service is still not running, that mean, the Connection Management dialog
        # has been closed or canceled. So, now, we just need to shut the application down.
        utils.exitApp()

    # Prefetch default containers for search
    containers_service.prefetchDefaultContainersInBackground()

    # Stop daemon before exit
    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
