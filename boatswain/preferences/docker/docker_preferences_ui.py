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
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QVBoxLayout

from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import AutoResizeWidget


class DockerPreferencesUi(AutoResizeWidget):

    def preferableSize(self) -> QSize:
        height = system_service.getRefHeight() / 2
        width = height * 1.8
        return QSize(width, height)

    def __init__(self, parent, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.vertical_layout_2 = QVBoxLayout(self)
        self.vertical_layout_2.setContentsMargins(rt(20), rt(11), rt(20), rt(11))
        self.vertical_layout_2.setSpacing(rt(6))
