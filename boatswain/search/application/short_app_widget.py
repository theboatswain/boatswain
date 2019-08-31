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

from PyQt5.QtCore import QCoreApplication

from boatswain.common.services import data_transporter_service, containers_service
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.common.utils.constants import CONTAINER_CHANNEL
from boatswain.search.application.short_app_widget_ui import ShortAppWidgetUi


class ShortAppWidget:

    _translate = QCoreApplication.translate
    template = 'ShortAppWidget'

    def __init__(self, parent_widget, name, description, repo, group) -> None:
        self.repo = repo
        self.ui = ShortAppWidgetUi(parent_widget, name, description, self)
        self.disable_button = False
        self.group = group
        if len(description) > 0:
            self.ui.description.setText(self._translate("widget", description))

        self.ui.from_repo.setText(self._translate(self.template, "From Dockerhub"))
        self.ui.install.setText(self._translate(self.template, "Install"))
        self.ui.name.setText(self._translate(self.template, name))

        if containers_service.isAppInstalled(name):
            self.ui.install.setText(self._translate("widget", "Installed"))
            self.disable_button = True

        self.ui.install.clicked.connect(self.installApp)

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
