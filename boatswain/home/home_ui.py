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

from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QSizePolicy, QLineEdit, QPushButton, \
    QMainWindow, QFrame, QScrollArea, QMenuBar, QMenu, QStatusBar, QAction, QLabel

from boatswain.common.services import data_transporter_service
from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.common.ui.select_ui import SelectUi
from boatswain.common.utils.constants import APP_EXIT_CHANNEL


class HomeUi(QMainWindow):
    """ Home screen """

    def __init__(self):
        super(HomeUi, self).__init__()
        self.setSizePolicy(BQSizePolicy(h_stretch=1))
        central_widget = QWidget(self)
        central_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, rt(6), 0, rt(11))
        main_layout.setSpacing(0)
        widget = QWidget(central_widget)
        widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        widget.setAutoFillBackground(False)
        top_layout = QGridLayout(widget)
        top_layout.setContentsMargins(rt(11), 0, rt(4), rt(6))
        top_layout.setSpacing(rt(6))

        self.add_app = QPushButton(widget)
        padding = "%dpx %dpx" % (rt(1), rt(12))
        self.add_app.setStyleSheet("border: 1px solid #999999; padding: %s; border-radius: 2px" % padding)
        self.add_app.setSizePolicy(BQSizePolicy(width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.add_app.setFocusPolicy(Qt.ClickFocus)
        top_layout.addWidget(self.add_app, 0, 0, 1, 1)

        self.workspaces = SelectUi(widget)
        self.workspaces.setSizePolicy(BQSizePolicy(h_stretch=1, width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.workspaces.setFocusPolicy(Qt.ClickFocus)
        top_layout.addWidget(self.workspaces, 0, 2, 1, 1)
        self.search_app = QLineEdit(widget)
        self.search_app.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.search_app.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.search_app.setFocusPolicy(Qt.ClickFocus)
        self.search_app.setStyleSheet("padding: 1 1 1 5;")
        top_layout.addWidget(self.search_app, 0, 3, 1, 1)
        self.custom_menu = QPushButton(widget)
        self.custom_menu.setText("⋮")
        self.custom_menu.setStyleSheet("border: none; padding: 1px 2px;")
        font = QFont()
        font.setPointSize(applyFontRatio(18))
        self.custom_menu.setFont(font)
        top_layout.addWidget(self.custom_menu, 0, 4, 1, 1)

        hidden_widget = QWidget(widget)
        hidden_widget.setSizePolicy(BQSizePolicy())
        top_layout.addWidget(hidden_widget, 0, 1, 1, 1)

        main_layout.addWidget(widget)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        self.scroll_area = QScrollArea(central_widget)
        self.scroll_area.setSizePolicy(BQSizePolicy(v_stretch=20))
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)
        self.setCentralWidget(central_widget)

        self.menu_bar = QMenuBar(self)
        self.menu_file = QMenu(self.menu_bar)
        self.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        self.retranslateUi(self)
        self.app_list = QWidget(self)
        self.app_list.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.app_list_layout = QVBoxLayout(self.app_list)
        self.app_list_layout.setSpacing(0)
        self.app_list_layout.setAlignment(Qt.AlignTop)
        self.app_list_layout.setContentsMargins(0, rt(1), 0, 0)
        self.app_list.setLayout(self.app_list_layout)
        self.scroll_area.setWidget(self.app_list)

    def retranslateUi(self, boatswain):
        _translate = QCoreApplication.translate
        boatswain.setWindowTitle(_translate("Boatswain", "Boatswain"))
        self.search_app.setPlaceholderText(_translate("Boatswain", "Filter apps"))
        self.add_app.setText(_translate("Boatswain", "Add"))

    def closeEvent(self, event):
        data_transporter_service.fire(APP_EXIT_CHANNEL)
        QMainWindow.closeEvent(self, event)
