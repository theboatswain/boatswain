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

import requests
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPixmap, QImage

from boatswain.common.services import data_transporter_service, containers_service
from boatswain.common.services.system_service import rt
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils.constants import CONTAINER_CHANNEL
from boatswain.common.utils.utils import tr
from boatswain.search.application.short_app_widget_ui import ShortAppWidgetUi


class ShortAppWidget:

    def __init__(self, parent_widget, container_info, group) -> None:
        self.repo = container_info['from']
        self.ui = ShortAppWidgetUi(parent_widget, self)
        self.disable_button = False
        self.group = group

        self.ui.from_repo.setText(tr("#Dockerhub"))
        self.ui.install.setText(tr("Install"))
        self.ui.name.setText(tr(container_info['name']))

        if containers_service.isAppInstalled(container_info['name']):
            self.ui.install.setText(tr("Installed"))
            self.ui.install.setStyleSheet('border: 1px solid gray; padding: 1px 6px; color: gray')
            self.disable_button = True

        self.ui.install.clicked.connect(self.installApp)
        if 'description' not in container_info:
            worker = Worker(containers_service.getContainerInfo, container_info['name'], container_info['is_official'])
            worker.signals.result.connect(self.showInfo)
            threadpool.start(worker)
        else:
            self.showInfo(container_info)
        if 'logo_url' not in container_info:
            worker = Worker(containers_service.getContainerLogo, container_info['name'])
            worker.signals.result.connect(self.showLogo)
            threadpool.start(worker)
        else:
            self.showLogo(container_info['logo_url'])

    def showLogo(self, logo):
        if logo is not None:
            worker = Worker(self.getImage, logo)
            worker.signals.result.connect(self.drawLogo)
            threadpool.start(worker, 99)

    def drawLogo(self, pixmap: QPixmap):
        try:
            self.ui.icon.setPixmap(pixmap)
            color = self.analyzeColor(pixmap.toImage())
            color_str = "rgb(%d, %d, %d)" % (color.red(), color.green(), color.blue())
            self.ui.avatar_area.setStyleSheet("background: %s" % color_str)
        except RuntimeError:
            pass

    def showInfo(self, container_info):
        try:
            if len(container_info['description']) > 0:
                self.ui.description.setText(self._translate("widget", container_info['description']))
            self.ui.stars.setText(tr("☆ " + str(container_info['star_count'])))

            if not container_info['is_official']:
                self.ui.is_official.hide()
            self.ui.is_official.setText(tr("⚜ Official"))
        except RuntimeError:
            pass

    def installApp(self):
        if self.disable_button:
            return
        self.disable_button = True
        self.ui.install.setText(tr("Installing"))
        worker = Worker(containers_service.installContainer, self.ui.name.text(), self.repo,
                        self.ui.description.text(), "latest", None, None, self.group)
        worker.signals.result.connect(self.onAppInstalled)
        threadpool.start(worker)

    def onAppInstalled(self, container):
        data_transporter_service.fire(CONTAINER_CHANNEL, container)
        try:
            self.ui.install.setText(tr("Installed"))
        except RuntimeError:
            # When user close the add app dialog before app is installed
            pass

    def getImage(self, url):
        data = requests.get(url)
        img = QImage()
        img.loadFromData(data.content)
        pixmap = QPixmap(img).scaledToWidth(rt(32), Qt.SmoothTransformation)
        return pixmap

    def analyzeColor(self, img: QImage):
        rect: QRect = img.rect()
        mid_top = QPoint(rect.width() / 2 + rect.x(), rect.y())
        top_color = self.getFirstColor(img, mid_top)
        return top_color.lighter(140)

    def getFirstColor(self, img: QImage, point: QPoint, x=False, unit=1):
        color = img.pixelColor(point)
        while color.alpha() == 0:
            if x:
                point.setX(point.x() + unit)
            else:
                point.setY(point.y() + unit)
            color = img.pixelColor(point)
        return color
