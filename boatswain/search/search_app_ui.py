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

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QFrame, QScrollArea, QLineEdit, QComboBox, QGridLayout

from boatswain.common.utils.custom_ui import BQSizePolicy


class SearchAppDialogUi(object):

    def __init__(self, dialog) -> None:
        super().__init__()
        dialog.resize(792, 387)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(792, 387))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)
        widget = QWidget(dialog)
        widget.setSizePolicy(BQSizePolicy())
        self.grid_container = QGridLayout(widget)
        self.grid_container.setContentsMargins(0, 0, 0, 0)
        self.repo_select = QComboBox(widget)
        self.repo_select.setSizePolicy(BQSizePolicy(width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.grid_container.addWidget(self.repo_select, 0, 0, 1, 1)
        self.key_search = QLineEdit(widget)
        self.key_search.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.key_search.setFocusPolicy(Qt.StrongFocus)
        self.key_search.setStyleSheet("padding: 2 2 2 5;")
        self.grid_container.addWidget(self.key_search, 0, 1, 1, 1)
        main_layout.addWidget(widget)
        self.scroll_area = QScrollArea(dialog)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.search_result_area = QWidget(dialog)
        self.search_result_area.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.search_result_area.setLayout(QVBoxLayout(self.search_result_area))
        self.search_result_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.search_result_area)
