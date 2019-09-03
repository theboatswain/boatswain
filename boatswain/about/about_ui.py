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

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QFrame, QSizePolicy

from boatswain.common.ui.custom_ui import BQSizePolicy

from boatswain.common.services import system_service


class AboutUi(object):

    def __init__(self, dialog) -> None:
        super().__init__()
        height = system_service.screen_height / 2.6
        width = height * 2
        dialog.resize(width, height)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(width, height))
        dialog.setMinimumSize(QSize(width, height))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)

        self.horizontal_layout = QtWidgets.QHBoxLayout(dialog)
        self.horizontal_layout.setContentsMargins(11, 11, 11, 11)
        self.horizontal_layout.setSpacing(6)
        self.left_widget = QtWidgets.QWidget(dialog)
        self.left_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.left_widget)
        self.vertical_layout_2.setContentsMargins(11, 11, 11, 11)
        self.vertical_layout_2.setSpacing(6)
        self.app_image_widget = QtWidgets.QWidget(self.left_widget)
        self.app_image_widget.setSizePolicy(BQSizePolicy(v_stretch=2))
        self.vertical_layout_4 = QtWidgets.QVBoxLayout(self.app_image_widget)
        self.vertical_layout_4.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_4.setSpacing(6)
        self.avatar = QtWidgets.QLabel(self.app_image_widget)
        self.avatar.setText("")
        self.avatar.setAlignment(QtCore.Qt.AlignCenter)
        self.vertical_layout_4.addWidget(self.avatar)
        self.vertical_layout_2.addWidget(self.app_image_widget)
        self.app_info_widget = QtWidgets.QWidget(self.left_widget)
        self.app_info_widget.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.app_info_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(6)
        self.boatswain = QtWidgets.QLabel(self.app_info_widget)
        font = QtGui.QFont()
        font.setPointSize(17)
        font.setWeight(50)
        self.boatswain.setFont(font)
        self.boatswain.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.boatswain)
        self.build = QtWidgets.QLabel(self.app_info_widget)
        self.build.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.build.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.build)
        self.license = QtWidgets.QPushButton(self.app_info_widget)
        self.verticalLayout_3.addWidget(self.license)
        self.vertical_layout_2.addWidget(self.app_info_widget)
        self.horizontal_layout.addWidget(self.left_widget)
        self.right_widget = QtWidgets.QWidget(dialog)
        self.right_widget.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.right_widget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.scroll_area = QtWidgets.QScrollArea(self.right_widget)
        self.scroll_area.setSizePolicy(BQSizePolicy(v_stretch=20))
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.addWidget(self.scroll_area)
        self.acknowledge_widget = QtWidgets.QWidget(self.right_widget)
        self.acknowledge_widget.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.acknowledge_layout = QtWidgets.QHBoxLayout(self.acknowledge_widget)
        self.acknowledge_layout.setContentsMargins(0, 10, 0, 0)
        self.acknowledge_layout.setSpacing(0)
        self.acknowledge_layout.setAlignment(Qt.AlignTop)
        self.acknowledge_widget.setLayout(self.acknowledge_layout)

        self.acknowledge = QtWidgets.QLabel(self.right_widget)
        self.acknowledge.setSizePolicy(BQSizePolicy())
        self.acknowledge.setTextFormat(Qt.RichText)
        self.acknowledge.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.acknowledge.setOpenExternalLinks(True)

        self.acknowledge_layout.addWidget(self.acknowledge)
        self.scroll_area.setWidget(self.acknowledge_widget)

        self.horizontal_layout.addWidget(self.right_widget)

        self.retranslateUi(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("dialog", "About"))
        self.boatswain.setText(_translate("dialog", "Boatswain v1.0.0"))
        self.build.setText(_translate("dialog", "Build 2021 (absjffs)"))
        self.license.setText(_translate("dialog", "License"))
