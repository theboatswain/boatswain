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

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QDialog, QSizePolicy

from boatswain.common.models.container import Container
from boatswain.common.services import system_service
from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.ui.custom_ui import BQSizePolicy, ButtonLineEdit
from boatswain.resources_utils import get_resource


class ShortcutCreatorUi:

    def __init__(self, dialog: QDialog, container: Container) -> None:
        self.container = container
        self.dialog = dialog
        height = system_service.screen_height / 2.2
        width = height * 2
        dialog.resize(width, height)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(width, height))
        dialog.setSizeGripEnabled(False)
        dialog.setWindowModality(Qt.WindowModal)
        self.vertical_layout = QtWidgets.QVBoxLayout(dialog)
        self.vertical_layout.setContentsMargins(rt(11), rt(11), rt(11), rt(11))
        self.vertical_layout.setSpacing(rt(6))
        self.stacked_widget = QtWidgets.QStackedWidget(dialog)
        self.first_step = QtWidgets.QWidget()
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.first_step)
        self.vertical_layout_2.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_2.setSpacing(rt(6))
        self.tab_widget = QtWidgets.QTabWidget(self.first_step)
        self.tab = QtWidgets.QWidget()
        self.vertical_layout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.vertical_layout_3.setContentsMargins(rt(11), rt(11), rt(11), rt(11))
        self.vertical_layout_3.setSpacing(rt(6))
        self.top_line = QtWidgets.QFrame(self.tab)
        self.top_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.top_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_layout_3.addWidget(self.top_line)
        self.main_widget = QtWidgets.QWidget(self.tab)
        self.main_widget.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.grid_layout = QtWidgets.QGridLayout(self.main_widget)
        self.grid_layout.setContentsMargins(rt(11), rt(11), rt(11), rt(11))
        self.grid_layout.setHorizontalSpacing(rt(6))
        self.grid_layout.setVerticalSpacing(0)
        self.label = QtWidgets.QLabel(self.main_widget)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.grid_layout.addWidget(self.label, 2, 0, 1, 1)
        self.label_des = QtWidgets.QLabel(self.main_widget)
        font = QtGui.QFont()
        font.setPointSize(applyFontRatio(11))
        self.label_des.setFont(font)
        self.label_des.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label_des.setWordWrap(True)
        self.label_des.setIndent(rt(2))
        self.grid_layout.addWidget(self.label_des, 3, 1, 1, 2)
        self.type_label = QtWidgets.QLabel(self.main_widget)
        self.type_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.grid_layout.addWidget(self.type_label, 4, 0, 1, 1)
        self.hidden = QtWidgets.QWidget(self.main_widget)
        self.hidden.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.grid_layout.addWidget(self.hidden, 0, 2, 1, 1)
        self.shortcut_for_label = QtWidgets.QLabel(self.main_widget)
        self.shortcut_for_label.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.shortcut_for_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.grid_layout.addWidget(self.shortcut_for_label, 0, 0, 1, 1)
        self.shortcut_label = QtWidgets.QLineEdit(self.main_widget)
        self.shortcut_label.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.shortcut_label.setStyleSheet("padding: 2 2 2 5;")
        self.grid_layout.addWidget(self.shortcut_label, 2, 1, 1, 1)
        self.shortcut_for_des = QtWidgets.QLabel(self.main_widget)
        self.shortcut_for_des.setSizePolicy(BQSizePolicy())
        self.shortcut_for_des.setFont(font)
        self.shortcut_for_des.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.shortcut_for_des.setWordWrap(True)
        self.shortcut_for_des.setIndent(2)
        self.grid_layout.addWidget(self.shortcut_for_des, 1, 1, 1, 2)
        self.container_name = QtWidgets.QComboBox(self.main_widget)
        self.container_name.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.grid_layout.addWidget(self.container_name, 0, 1, 1, 1)
        self.data_type_label = QtWidgets.QLabel(self.main_widget)
        self.data_type_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.grid_layout.addWidget(self.data_type_label, 5, 0, 1, 1)
        self.shortcut_type = QtWidgets.QComboBox(self.main_widget)
        self.grid_layout.addWidget(self.shortcut_type, 4, 1, 1, 1)
        self.data_type = QtWidgets.QComboBox(self.main_widget)
        self.grid_layout.addWidget(self.data_type, 5, 1, 1, 1)
        self.data_type_des = QtWidgets.QLabel(self.main_widget)
        self.data_type_des.setFont(font)
        self.data_type_des.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.data_type_des.setWordWrap(True)
        self.data_type_des.setIndent(2)
        self.grid_layout.addWidget(self.data_type_des, 6, 1, 1, 2)
        self.vertical_layout_3.addWidget(self.main_widget)
        self.bot_line = QtWidgets.QFrame(self.tab)
        self.bot_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.bot_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_layout_3.addWidget(self.bot_line)
        self.widget_2 = QtWidgets.QWidget(self.tab)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(rt(6))
        self.hidden_2 = QtWidgets.QWidget(self.widget_2)
        self.hidden_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.hidden_2)
        self.cancel_button = QtWidgets.QPushButton(self.widget_2)
        self.horizontal_layout.addWidget(self.cancel_button)
        self.next_button = QtWidgets.QPushButton(self.widget_2)
        self.horizontal_layout.addWidget(self.next_button)
        self.vertical_layout_3.addWidget(self.widget_2)
        self.tab_widget.addTab(self.tab, "")
        self.vertical_layout_2.addWidget(self.tab_widget)
        self.stacked_widget.addWidget(self.first_step)
        self.second_step = QtWidgets.QWidget()
        self.vertical_layout_4 = QtWidgets.QVBoxLayout(self.second_step)
        self.vertical_layout_4.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout_4.setSpacing(rt(6))
        self.tab_widget_2 = QtWidgets.QTabWidget(self.second_step)
        self.tab_3 = QtWidgets.QWidget()
        self.vertical_layout_5 = QtWidgets.QVBoxLayout(self.tab_3)
        self.vertical_layout_5.setContentsMargins(rt(11), rt(11), rt(11), rt(11))
        self.vertical_layout_5.setSpacing(rt(6))
        self.line_2 = QtWidgets.QFrame(self.tab_3)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_layout_5.addWidget(self.line_2)
        self.widget = QtWidgets.QWidget(self.tab_3)
        self.widget.setSizePolicy(BQSizePolicy(v_stretch=1))
        self.grid_layout_2 = QtWidgets.QGridLayout(self.widget)
        self.grid_layout_2.setContentsMargins(rt(11), rt(11), rt(11), rt(11))
        self.grid_layout_2.setHorizontalSpacing(rt(6))
        self.grid_layout_2.setVerticalSpacing(rt(5))
        self.mapping_to = QtWidgets.QLineEdit(self.widget)
        self.mapping_to.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.grid_layout_2.addWidget(self.mapping_to, 2, 1, 1, 1)
        self.description = QtWidgets.QTextEdit(self.widget)
        self.description.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.description.setMaximumHeight(rt(60))
        self.grid_layout_2.addWidget(self.description, 4, 1, 1, 2)
        self.default_value = ButtonLineEdit(get_resource('resources/icons/folder.svg'), self.widget)
        self.default_value.setSizePolicy(BQSizePolicy(h_stretch=2,
                                                      width=QSizePolicy.Expanding, height=QSizePolicy.Fixed))
        self.grid_layout_2.addWidget(self.default_value, 0, 1, 1, 1)
        self.mapping_to_label = QtWidgets.QLabel(self.widget)
        self.mapping_to_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.grid_layout_2.addWidget(self.mapping_to_label, 2, 0, 1, 1)
        self.description_label = QtWidgets.QLabel(self.widget)
        self.description_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.grid_layout_2.addWidget(self.description_label, 4, 0, 1, 1)
        self.default_value_label = QtWidgets.QLabel(self.widget)
        self.default_value_label.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.default_value_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.grid_layout_2.addWidget(self.default_value_label, 0, 0, 1, 1)
        self.hidden_3 = QtWidgets.QWidget(self.widget)
        self.hidden_3.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.grid_layout_2.addWidget(self.hidden_3, 0, 2, 1, 1)
        self.default_value_des = QtWidgets.QLabel(self.widget)
        self.default_value_des.setFont(font)
        self.default_value_des.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.default_value_des.setWordWrap(True)
        self.grid_layout_2.addWidget(self.default_value_des, 1, 1, 1, 2)
        self.mapping_to_des = QtWidgets.QLabel(self.widget)
        self.mapping_to_des.setFont(font)
        self.mapping_to_des.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.grid_layout_2.addWidget(self.mapping_to_des, 3, 1, 1, 2)
        self.vertical_layout_5.addWidget(self.widget)
        self.line = QtWidgets.QFrame(self.tab_3)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_layout_5.addWidget(self.line)
        self.bot_widget = QtWidgets.QWidget(self.tab_3)
        self.horizontal_layout_2 = QtWidgets.QHBoxLayout(self.bot_widget)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(rt(6))
        self.widget_4 = QtWidgets.QWidget(self.bot_widget)
        self.widget_4.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout_2.addWidget(self.widget_4)
        self.back_button = QtWidgets.QPushButton(self.bot_widget)
        self.horizontal_layout_2.addWidget(self.back_button)
        self.cancel_button_2 = QtWidgets.QPushButton(self.bot_widget)
        self.horizontal_layout_2.addWidget(self.cancel_button_2)
        self.finish_button = QtWidgets.QPushButton(self.bot_widget)
        self.horizontal_layout_2.addWidget(self.finish_button)
        self.vertical_layout_5.addWidget(self.bot_widget)
        self.tab_widget_2.addTab(self.tab_3, "")
        self.vertical_layout_4.addWidget(self.tab_widget_2)
        self.stacked_widget.addWidget(self.second_step)
        self.vertical_layout.addWidget(self.stacked_widget)

        self.stacked_widget.setCurrentIndex(0)
        self.tab_widget.setCurrentIndex(0)
        self.default_value.button.setVisible(False)
