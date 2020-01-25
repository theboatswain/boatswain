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

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QFrame, QScrollArea, QLineEdit, QGridLayout

from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.common.ui.select_ui import SelectUi


class SearchAppDialogUi(object):

    def __init__(self, dialog) -> None:
        super().__init__()
        height = system_service.getRefHeight() / 1.8
        width = height * 1.8
        dialog.resize(width, height)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(width, height))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(rt(8), rt(8), rt(8), rt(8))
        main_layout.setSpacing(0)
        widget = QWidget(dialog)
        widget.setSizePolicy(BQSizePolicy())
        self.grid_container = QGridLayout(widget)
        self.grid_container.setContentsMargins(0, 0, 0, rt(10))
        self.repo_select = SelectUi(widget)
        self.repo_select.setSizePolicy(BQSizePolicy(width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.grid_container.addWidget(self.repo_select, 0, 0, 1, 1)
        self.key_search = QLineEdit(widget)
        self.key_search.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.key_search.setFocusPolicy(Qt.StrongFocus)
        self.key_search.setProperty('class', 'bordered-widget')
        self.key_search.setStyleSheet("padding: 0 0 0 5;")
        self.grid_container.addWidget(self.key_search, 0, 1, 1, 1)
        main_layout.addWidget(widget)
        self.scroll_area = QScrollArea(dialog)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.search_result_area = QWidget(dialog)
        self.search_result_area.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.search_result_layout = QGridLayout(self.search_result_area)
        self.search_result_layout.setContentsMargins(rt(10), rt(10), rt(12), rt(10))
        self.search_result_layout.setAlignment(QtCore.Qt.AlignTop)
        self.search_result_area.setLayout(self.search_result_layout)
        # self.search_result_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.search_result_area)
