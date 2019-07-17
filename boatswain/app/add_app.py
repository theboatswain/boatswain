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

from PyQt5.QtCore import Qt, QCoreApplication, QMetaObject, QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QFrame, QScrollArea, QLineEdit, QComboBox, QGridLayout

from boatswain.app.add_app_widget import AddAppWidget
from boatswain.app.default_search_result import search_result
from boatswain.common.services import containers_service
from boatswain.common.utils.custom_ui import BQSizePolicy


class AddAppDialog(object):

    def __init__(self, title, dialog) -> None:
        super().__init__()
        self.title = title
        self.setup_ui(dialog)
        dialog.setWindowTitle(self.title)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.search_result_area = QWidget(dialog)
        self.search_result_area.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.search_result_area.setLayout(QVBoxLayout(self.search_result_area))
        self.search_result_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidget(self.search_result_area)
        self.key_search.returnPressed.connect(self.search_app)

        # Loading default search images
        self.load_result(search_result)

    def setup_ui(self, add_app_dialog):
        add_app_dialog.resize(792, 387)
        add_app_dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        add_app_dialog.setMinimumSize(QSize(792, 387))
        add_app_dialog.setSizeGripEnabled(False)
        add_app_dialog.setModal(False)
        main_layout = QVBoxLayout(add_app_dialog)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)
        widget = QWidget(add_app_dialog)
        widget.setSizePolicy(BQSizePolicy())
        self.grid_container = QGridLayout(widget)
        self.grid_container.setContentsMargins(0, 0, 0, 0)
        self.combo_box = QComboBox(widget)
        self.combo_box.setSizePolicy(BQSizePolicy(width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.combo_box.addItem("")
        self.grid_container.addWidget(self.combo_box, 0, 0, 1, 1)
        self.key_search = QLineEdit(widget)
        self.key_search.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.key_search.setFocusPolicy(Qt.StrongFocus)
        self.key_search.setStyleSheet("padding: 2 2 2 5;")
        self.key_search.setObjectName("keySearch")
        self.grid_container.addWidget(self.key_search, 0, 1, 1, 1)
        main_layout.addWidget(widget)
        self.scroll_area = QScrollArea(add_app_dialog)
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        main_layout.addWidget(self.scroll_area)

        self.retranslate_ui(add_app_dialog)
        QMetaObject.connectSlotsByName(add_app_dialog)

    def retranslate_ui(self, add_app_dialog):
        _translate = QCoreApplication.translate
        add_app_dialog.setWindowTitle(_translate("addAppDialog", "Dialog"))
        self.combo_box.setItemText(0, _translate("addAppDialog", "All repos"))
        self.key_search.setPlaceholderText(_translate("addAppDialog", "Search apps"))

    def search_app(self):
        keyword = self.key_search.text()
        if len(keyword) == 0:
            return
        docker_images = containers_service.searchImages(keyword, self.combo_box.currentText())
        self.load_result(docker_images)

    def load_result(self, docker_images):
        self.clean_search_results()
        for item in docker_images:
            widget = AddAppWidget(self.search_result_area, item['name'], item['description'],
                                  item['from'])
            self.search_result_area.layout().addWidget(widget)

    def clean_search_results(self):
        while self.search_result_area.layout().count():
            item = self.search_result_area.layout().takeAt(0)
            item.widget().deleteLater()
