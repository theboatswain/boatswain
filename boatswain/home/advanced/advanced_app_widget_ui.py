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

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QWidget, QSizePolicy, QPushButton, QLabel, QComboBox, QFrame, QVBoxLayout, QHBoxLayout

from boatswain.common.models.container import Container
from boatswain.common.utils.custom_ui import BQSizePolicy


class AdvancedAppWidgetUi(QWidget):

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 3, 0)
        self.layout.setSpacing(6)
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)
        self.widget = QWidget(self)
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(6)
        self.label = QLabel(self.widget)
        self.horizontal_layout.addWidget(self.label)
        self.tags = QComboBox(self.widget)
        self.tags.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.horizontal_layout.addWidget(self.tags)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.widget_2)
        self.layout.addWidget(self.widget)
        self.widget_3 = QWidget(self)
        self.horizontal_layout_2 = QHBoxLayout(self.widget_3)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(6)
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout_2.addWidget(self.widget_4)
        self.advanced_configuration = QPushButton(self.widget_3)
        self.horizontal_layout_2.addWidget(self.advanced_configuration)
        self.layout.addWidget(self.widget_3)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.label.setText(_translate("AdvancedWidget", "Image tag:"))
        self.advanced_configuration.setText(_translate("AdvancedWidget", "Advanced configuration"))
