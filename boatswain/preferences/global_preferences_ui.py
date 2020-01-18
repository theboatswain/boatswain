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

from PyQt5.QtCore import QSize, QObject
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QDialog

from boatswain.common.services import system_service
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.common.utils.utils import tr
from boatswain.preferences.docker.docker_preferences import DockerPreferences
from boatswain.preferences.general.general_preferences import GeneralPreferences
from boatswain.preferences.startup.startup_preferences import StartupPreferences
from boatswain.preferences.workspace.workspace_preferences import WorkspacePreferences


class GlobalPreferencesUi(QObject):

    def __init__(self, dialog: QDialog) -> None:
        super().__init__()

        height = system_service.getRefHeight() / 2
        width = height * 1.8
        dialog.resize(width, height)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(width, height))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)

        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.central_widget = QWidget(dialog)
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.vertical_layout.setContentsMargins(11, 11, 11, 15)
        self.vertical_layout.setSpacing(6)
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setDocumentMode(False)
        self.general = GeneralPreferences(self.central_widget)
        self.tab_widget.addTab(self.general.ui, tr("General"))

        self.docker = DockerPreferences(self.central_widget)
        self.tab_widget.addTab(self.docker.ui, tr("Docker"))

        self.workspace = WorkspacePreferences(self.central_widget)
        self.tab_widget.addTab(self.workspace.ui, tr("Workspaces"))

        self.startup = StartupPreferences(self.central_widget)
        self.tab_widget.addTab(self.startup.ui, tr("Startup"))
        self.vertical_layout.addWidget(self.tab_widget)

        main_layout.addWidget(self.central_widget)
