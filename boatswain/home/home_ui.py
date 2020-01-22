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
import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QPalette, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QSizePolicy, QLineEdit, QPushButton, \
    QMainWindow, QFrame, QScrollArea, QMenuBar, QMenu, QStatusBar, QHBoxLayout

from boatswain.common.services import data_transporter_service
from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.common.ui.select_ui import SelectUi
from boatswain.common.utils.constants import APP_EXIT_CHANNEL
from boatswain.common.utils.utils import tr


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
        top_layout = QHBoxLayout(widget)
        top_layout.setContentsMargins(rt(11), 0, rt(4), rt(6))
        top_layout.setSpacing(rt(6))

        self.add_app = QPushButton(widget)
        self.add_app.setFlat(True)
        self.add_app.setProperty('class', 'border-button')
        self.add_app.setStyleSheet("padding: %dpx %dpx" % (rt(1), rt(12)))
        self.add_app.setSizePolicy(BQSizePolicy(width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.add_app.setFocusPolicy(Qt.ClickFocus)
        top_layout.addWidget(self.add_app)

        self.workspaces = SelectUi(widget)
        self.workspaces.setSizePolicy(BQSizePolicy(h_stretch=1, width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.workspaces.setFocusPolicy(Qt.ClickFocus)
        top_layout.addWidget(self.workspaces)
        self.search_app = QLineEdit(widget)
        self.search_app.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.search_app.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.search_app.setFocusPolicy(Qt.ClickFocus)
        self.search_app.setStyleSheet("padding: 0 0 0 5; background-color: transparent;")
        self.search_app.setProperty('class', 'border-button')
        top_layout.addWidget(self.search_app)
        self.custom_menu = QPushButton(widget)
        self.custom_menu.setText("⋮")
        self.custom_menu.setFlat(True)
        self.custom_menu.setStyleSheet("border: none; padding: 1px 2px;")
        font = QFont()
        font.setPointSize(applyFontRatio(16))
        self.custom_menu.setFont(font)
        top_layout.addWidget(self.custom_menu)

        hidden_widget = QWidget(widget)
        hidden_widget.setSizePolicy(BQSizePolicy())
        top_layout.addWidget(hidden_widget)

        main_layout.addWidget(widget)

        line = QFrame(self)
        line.setLineWidth(0)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        main_layout.addWidget(line)

        self.scroll_area = QScrollArea(central_widget)
        self.scroll_area.setStyleSheet('background-color: transparent')
        self.scroll_area.verticalScrollBar().resize(0, 0)
        self.scroll_area.horizontalScrollBar().resize(0, 0)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setSizePolicy(BQSizePolicy(v_stretch=2))
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
        self.setProperty('class', 'home')

    def retranslateUi(self, boatswain):
        boatswain.setWindowTitle("Boatswain")
        self.search_app.setPlaceholderText(tr("Filter apps"))
        self.add_app.setText(tr("Add"))

    def setBackgroundImage(self, image_path):
        if os.path.isfile(image_path):
            pixmap = QPixmap(image_path)
            pixmap = pixmap.scaled(self.size(), Qt.IgnoreAspectRatio)
            palette = self.palette()
            palette.setBrush(QPalette.Background, QBrush(pixmap))
            self.setPalette(palette)
            self.update()

    def setBackgroundColor(self, color: QColor):
        palette = self.palette()
        palette.setBrush(QPalette.Background, QBrush(color))
        self.setPalette(palette)
        self.update()

    def closeEvent(self, event):
        data_transporter_service.fire(APP_EXIT_CHANNEL)
        QMainWindow.closeEvent(self, event)
