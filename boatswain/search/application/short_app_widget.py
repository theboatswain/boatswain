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
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#
import requests
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QPixmap, QImage

from boatswain.common.services import data_transporter_service, containers_service
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils.constants import CONTAINER_CHANNEL
from boatswain.search.application.short_app_widget_ui import ShortAppWidgetUi


class ShortAppWidget:

    _translate = QCoreApplication.translate
    template = 'ShortAppWidget'

    def __init__(self, parent_widget, container_info, group) -> None:
        self.repo = container_info['from']
        self.ui = ShortAppWidgetUi(parent_widget, self)
        self.disable_button = False
        self.group = group
        if len(container_info['description']) > 0:
            self.ui.description.setText(self._translate("widget", container_info['description']))

        self.ui.from_repo.setText(self._translate(self.template, "#Dockerhub"))
        self.ui.install.setText(self._translate(self.template, "Install"))
        self.ui.name.setText(self._translate(self.template, container_info['name']))
        if not container_info['is_official']:
            self.ui.is_official.hide()
        self.ui.is_official.setText("⚜ Official")
        self.ui.stars.setText(self._translate(self.template, "☆ " + str(container_info['star_count'])))

        if containers_service.isAppInstalled(container_info['name']):
            self.ui.install.setText(self._translate("widget", "Installed"))
            self.disable_button = True

        self.ui.install.clicked.connect(self.installApp)
        if 'logo_url' in container_info:
            worker = Worker(self.getImage, container_info['logo_url'])
            worker.signals.result.connect(lambda x: self.ui.icon.setPixmap(x))
            threadpool.start(worker)

    def installApp(self):
        if self.disable_button:
            return
        self.disable_button = True
        self.ui.install.setText(self._translate(self.template, "Installing"))
        worker = Worker(containers_service.installContainer, self.ui.name.text(), self.repo,
                        self.ui.description.text(), "latest", None, None, self.group)
        worker.signals.result.connect(self.onAppInstalled)
        threadpool.start(worker)

    def onAppInstalled(self, container):
        data_transporter_service.fire(CONTAINER_CHANNEL, container)
        self.ui.install.setText(self._translate(self.template, "Installed"))

    def getImage(self, url):
        data = requests.get(url)
        img = QImage()
        img.loadFromData(data.content)
        pixmap = QPixmap(img).scaledToHeight(32, Qt.SmoothTransformation)
        return pixmap
