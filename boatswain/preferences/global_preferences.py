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

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from boatswain.common.utils.utils import tr
from boatswain.preferences.global_preferences_ui import GlobalPreferencesUi


class GlobalPreferences:

    def __init__(self, parent) -> None:
        super().__init__()
        self.dialog = QDialog(parent)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)

        self.ui = GlobalPreferencesUi(self.dialog)
        self.dialog.ui = self.ui

        self.ui.tab_widget.currentChanged.connect(self.onTabChange)

        self.dialog.setWindowTitle(tr("Preferences"))
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)

    def show(self):
        self.dialog.exec_()

    def onTabChange(self, index):
        widget = self.ui.tab_widget.widget(index)
        self.dialog.setMinimumSize(widget.preferableSize())
        self.dialog.resize(widget.preferableSize())