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
from PyQt5.QtWidgets import QWidget, QSizePolicy, QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout

from boatswain.common.models.container import Container
from boatswain.common.services.system_service import rt
from boatswain.common.utils.custom_ui import BQSizePolicy


class AdvancedAppWidgetUi(QWidget):

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(rt(20), 0, rt(3), rt(5))
        self.layout.setSpacing(rt(6))
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)
        self.widget = QWidget(self)
        self.grid_layout = QGridLayout(self.widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(rt(6))
        self.layout.addWidget(self.widget)
        self.widget_3 = QWidget(self)
        self.horizontal_layout_2 = QHBoxLayout(self.widget_3)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(rt(6))
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout_2.addWidget(self.widget_4)
        # self.advanced_configuration = QPushButton(self.widget_3)
        # self.horizontal_layout_2.addWidget(self.advanced_configuration)
        self.layout.addWidget(self.widget_3)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        # self.advanced_configuration.setText(_translate("AdvancedWidget", "Advanced configuration"))
