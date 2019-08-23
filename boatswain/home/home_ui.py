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
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QComboBox, QSizePolicy, QLineEdit, QPushButton, \
    QMainWindow, QFrame, QScrollArea, QMenuBar, QMenu, QStatusBar, QAction, QApplication

from boatswain.common.services import data_transporter_service
from boatswain.common.services.system_service import applyRatio
from boatswain.common.utils.constants import APP_EXIT_CHANNEL
from boatswain.common.utils.custom_ui import BQSizePolicy


class HomeUi(QMainWindow):
    """ Home screen """

    def __init__(self):
        super(HomeUi, self).__init__()
        self.setSizePolicy(BQSizePolicy(h_stretch=1))
        central_widget = QWidget(self)
        central_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, applyRatio(3), 0, applyRatio(11))
        main_layout.setSpacing(0)
        widget = QWidget(central_widget)
        widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        widget.setAutoFillBackground(False)
        top_layout = QGridLayout(widget)
        top_layout.setContentsMargins(applyRatio(11), 0, applyRatio(11), applyRatio(6))
        top_layout.setSpacing(applyRatio(6))

        self.add_app = QPushButton(widget)
        # self.add_app.setFixedHeight(applyRatio(24))
        self.add_app.setSizePolicy(BQSizePolicy(width=QSizePolicy.Minimum, height=QSizePolicy.Fixed))
        self.add_app.setFocusPolicy(Qt.ClickFocus)
        top_layout.addWidget(self.add_app, 0, 0, 1, 1)

        self.app_type = QComboBox(widget)
        self.app_type.setSizePolicy(BQSizePolicy(h_stretch=1, width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.app_type.setFixedHeight(applyRatio(24))
        self.app_type.setFocusPolicy(Qt.ClickFocus)
        top_layout.addWidget(self.app_type, 0, 2, 1, 1)
        self.search_app = QLineEdit(widget)
        self.search_app.setFixedHeight(applyRatio(22))
        self.search_app.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.search_app.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.search_app.setFocusPolicy(Qt.ClickFocus)
        self.search_app.setStyleSheet("padding: 2 2 2 5;")
        top_layout.addWidget(self.search_app, 0, 3, 1, 1)

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
        self.action_add = QAction(self)
        self.menu_file.addAction(self.action_add)
        self.menu_bar.addAction(self.menu_file.menuAction())

        self.menu_help = QMenu(self.menu_bar)
        self.about = QAction(self)
        self.about.setMenuRole(QAction.AboutRole)
        self.menu_help.addAction(self.about)
        self.check_for_update = QAction(self)
        self.check_for_update.setMenuRole(QAction.ApplicationSpecificRole)
        self.menu_help.addAction(self.check_for_update)
        self.menu_bar.addAction(self.menu_help.menuAction())

        self.retranslateUi(self)
        self.app_list = QWidget(self)
        self.app_list.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        layout = QVBoxLayout(self.app_list)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, applyRatio(1), 0, 0)
        self.app_list.setLayout(layout)
        self.scroll_area.setWidget(self.app_list)

    def retranslateUi(self, boatswain):
        _translate = QCoreApplication.translate
        boatswain.setWindowTitle(_translate("Boatswain", "Boatswain"))
        self.search_app.setPlaceholderText(_translate("Boatswain", "Filter apps"))
        self.add_app.setText(_translate("Boatswain", "Add"))
        self.menu_file.setTitle(_translate("Boatswain", "File"))
        self.action_add.setText(_translate("Boatswain", "Add new app"))
        self.check_for_update.setText(_translate("Boatswain", "Check for updates"))

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)

    def closeEvent(self, event):
        data_transporter_service.fire(APP_EXIT_CHANNEL, True)
        QMainWindow.closeEvent(self, event)
