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
import math
from typing import List

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QDialog

from boatswain.common.models.group import Group
from boatswain.common.services import containers_service
from boatswain.common.utils.constants import SEARCH_APP_WIDTH
from boatswain.search.application.short_app_widget import ShortAppWidget
from boatswain.search.search_app_ui import SearchAppDialogUi


class SearchAppDialog(object):

    _translate = QCoreApplication.translate
    template = 'SearchAppDialog'
    items_per_row = 3
    repositories = ['All repos']
    apps: List[ShortAppWidget] = []

    def __init__(self, title, parent, group: Group) -> None:
        super().__init__()
        self.default_containers = ['wordpress', 'mysql', 'mongo', 'mariadb', 'arangodb', 'postgres', 'django',
                                   'redis', 'memcached', 'nginx', 'tomcat']
        for index, item in enumerate(self.default_containers):
            self.default_containers[index] = {'name': item, 'from': 'dockerhub', 'is_official': True}
        self.title = title
        self.dialog = QDialog(parent)
        self.ui = SearchAppDialogUi(self.dialog)
        self.dialog.ui = self.ui
        self.dialog.setWindowTitle(self.title)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.group = group

        for repo in self.repositories:
            self.ui.repo_select.addItem(self._translate(self.template, repo))

        self.ui.key_search.setPlaceholderText(self._translate(self.template, "Search apps"))
        self.ui.key_search.returnPressed.connect(self.searchApp)

        # Loading default search images
        self.loadResult(self.default_containers)
        self.dialog.resizeEvent = self.resizeEvent

    def searchApp(self):
        keyword = self.ui.key_search.text()
        if len(keyword) != 0:
            docker_images = containers_service.searchImages(keyword, self.ui.repo_select.currentText())
        else:
            docker_images = self.default_containers
        self.loadResult(docker_images)

    def loadResult(self, docker_images):
        self.apps.clear()
        self.cleanSearchResults()
        col = 0
        row = 0
        self.items_per_row = math.trunc(self.dialog.size().width() / float(SEARCH_APP_WIDTH))
        for item in docker_images:
            widget = ShortAppWidget(self.ui.search_result_area, item, self.group)
            if col == self.items_per_row:
                col = 0
                row += 1
            self.ui.search_result_area.layout().addWidget(widget.ui, row, col, 1, 1)
            self.apps.append(widget)
            col += 1

    def cleanSearchResults(self):
        while self.ui.search_result_area.layout().count():
            item = self.ui.search_result_area.layout().takeAt(0)
            item.widget().deleteLater()

    def show(self):
        self.dialog.exec_()

    def resizeEvent(self, event: QResizeEvent):
        if math.trunc(event.size().width() / float(SEARCH_APP_WIDTH)) != self.items_per_row:
            col = 0
            row = 0
            self.items_per_row = math.trunc(self.dialog.size().width() / float(SEARCH_APP_WIDTH))
            for widget in self.apps:
                if col == self.items_per_row:
                    col = 0
                    row += 1
                widget.ui.parentWidget().layout().removeWidget(widget.ui)
                self.ui.search_result_area.layout().addWidget(widget.ui, row, col, 1, 1)
                col += 1
        QDialog.resizeEvent(self.dialog, event)
