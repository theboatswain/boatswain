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
from PyQt5.QtWidgets import QDialog, QWidget

from boatswain.common.models.container import Container
from boatswain.shortcut.create.shortcut_creator_ui import ShortcutCreatorUi


class ShortcutCreator:

    def __init__(self, container: Container, widget: QWidget) -> None:
        self.dialog = QDialog(widget)
        self.dialog.ui = ShortcutCreatorUi(self.dialog, container)

    def show(self):
        self.dialog.exec_()
