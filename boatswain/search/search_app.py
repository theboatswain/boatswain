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

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QDialog

from boatswain.common.services import containers_service
from boatswain.search.application.short_app_widget import ShortAppWidget
from boatswain.resources.default_search_result import search_result
from boatswain.search.search_app_ui import SearchAppDialogUi


class SearchAppDialog(object):

    _translate = QCoreApplication.translate
    template = 'SearchAppDialog'

    repositories = ['All repos']

    def __init__(self, title, parent) -> None:
        super().__init__()
        self.title = title
        self.dialog = QDialog(parent)
        self.ui = SearchAppDialogUi(self.dialog)
        self.dialog.ui = self.ui
        self.dialog.setWindowTitle(self.title)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)

        for repo in self.repositories:
            self.ui.repo_select.addItem(self._translate(self.template, repo))

        self.ui.key_search.setPlaceholderText(self._translate(self.template, "Search apps"))
        self.ui.key_search.returnPressed.connect(self.searchApp)

        # Loading default search images
        self.loadResult(search_result)

    def searchApp(self):
        keyword = self.ui.key_search.text()
        if len(keyword) == 0:
            return
        docker_images = containers_service.searchImages(keyword, self.ui.repo_select.currentText())
        self.loadResult(docker_images)

    def loadResult(self, docker_images):
        self.cleanSearchResults()
        for item in docker_images:
            widget = ShortAppWidget(self.ui.search_result_area, item['name'], item['description'], item['from'])
            self.ui.search_result_area.layout().addWidget(widget.ui)

    def cleanSearchResults(self):
        while self.ui.search_result_area.layout().count():
            item = self.ui.search_result_area.layout().takeAt(0)
            item.widget().deleteLater()

    def show(self):
        self.dialog.exec_()
