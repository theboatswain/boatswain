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

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QDialog, QSizePolicy

from boatswain.common.models.container import Container
from boatswain.common.utils.custom_ui import BQSizePolicy


class PreferencesShortcutCreator:

    def __init__(self, dialog: QDialog, container: Container) -> None:
        self.container = container
        self.dialog = dialog
        dialog.resize(749, 376)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(749, 376))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        self.vertical_layout = QtWidgets.QVBoxLayout(dialog)
        self.vertical_layout.setContentsMargins(11, 11, 11, 11)
        self.vertical_layout.setSpacing(6)
        self.top_widget = QtWidgets.QWidget(dialog)
        self.top_widget_layout = QtWidgets.QVBoxLayout(self.top_widget)
        self.top_widget_layout.setContentsMargins(11, 11, 11, 11)
        self.top_widget_layout.setSpacing(6)
        self.title = QtWidgets.QLabel(self.top_widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setWeight(50)
        self.title.setFont(font)
        self.top_widget_layout.addWidget(self.title)
        self.vertical_layout.addWidget(self.top_widget)
        self.top_line = QtWidgets.QFrame(dialog)
        self.top_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.top_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_layout.addWidget(self.top_line)
        self.mid_widget = QtWidgets.QWidget(dialog)
        self.mid_widget.setSizePolicy(BQSizePolicy(v_stretch=3))
        self.mid_widget_layout = QtWidgets.QGridLayout(self.mid_widget)
        self.mid_widget_layout.setContentsMargins(11, 11, 11, 11)
        self.mid_widget_layout.setHorizontalSpacing(6)
        self.mid_widget_layout.setVerticalSpacing(0)
        self.shortcut_type = QtWidgets.QComboBox(self.mid_widget)
        self.mid_widget_layout.addWidget(self.shortcut_type, 4, 1, 1, 1)
        self.shortcut_label = QtWidgets.QLineEdit(self.mid_widget)
        self.shortcut_label.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.shortcut_label.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.mid_widget_layout.addWidget(self.shortcut_label, 2, 1, 1, 1)
        self.data_type_label = QtWidgets.QLabel(self.mid_widget)
        self.data_type_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.mid_widget_layout.addWidget(self.data_type_label, 5, 0, 1, 1)
        self.data_type = QtWidgets.QComboBox(self.mid_widget)
        self.mid_widget_layout.addWidget(self.data_type, 5, 1, 1, 1)
        self.label_des = QtWidgets.QLabel(self.mid_widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_des.setFont(font)
        self.label_des.setWordWrap(True)
        self.label_des.setIndent(7)
        self.mid_widget_layout.addWidget(self.label_des, 3, 1, 1, 2)
        self.type_label = QtWidgets.QLabel(self.mid_widget)
        self.type_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.mid_widget_layout.addWidget(self.type_label, 4, 0, 1, 1)
        self.shortcut_for_des = QtWidgets.QLabel(self.mid_widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.shortcut_for_des.setFont(font)
        self.shortcut_for_des.setWordWrap(True)
        self.shortcut_for_des.setIndent(7)
        self.mid_widget_layout.addWidget(self.shortcut_for_des, 1, 1, 1, 2)
        self.shortcut_for_label = QtWidgets.QLabel(self.mid_widget)
        self.shortcut_for_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.mid_widget_layout.addWidget(self.shortcut_for_label, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.mid_widget)
        self.label.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.mid_widget_layout.addWidget(self.label, 2, 0, 1, 1)
        self.data_type_des = QtWidgets.QLabel(self.mid_widget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.data_type_des.setFont(font)
        self.data_type_des.setWordWrap(True)
        self.data_type_des.setIndent(7)
        self.mid_widget_layout.addWidget(self.data_type_des, 6, 1, 1, 2)
        self.hidden = QtWidgets.QWidget(self.mid_widget)
        self.hidden.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.mid_widget_layout.addWidget(self.hidden, 2, 2, 1, 1)
        self.container_name = QtWidgets.QComboBox(self.mid_widget)
        self.mid_widget_layout.addWidget(self.container_name, 0, 1, 1, 1)
        self.vertical_layout.addWidget(self.mid_widget)
        self.bot_line = QtWidgets.QFrame(dialog)
        self.bot_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.bot_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.vertical_layout.addWidget(self.bot_line)
        self.bot_widget = QtWidgets.QWidget(dialog)
        self.bot_widget_layout = QtWidgets.QHBoxLayout(self.bot_widget)
        self.bot_widget_layout.setContentsMargins(11, 11, 11, 11)
        self.bot_widget_layout.setSpacing(6)
        self.hidden_2 = QtWidgets.QWidget(self.bot_widget)
        self.hidden_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.bot_widget_layout.addWidget(self.hidden_2)
        self.cancel_button = QtWidgets.QPushButton(self.bot_widget)
        self.cancel_button.setObjectName("cancel_button")
        self.bot_widget_layout.addWidget(self.cancel_button)
        self.next_button = QtWidgets.QPushButton(self.bot_widget)
        self.next_button.setObjectName("next_button")
        self.bot_widget_layout.addWidget(self.next_button)
        self.vertical_layout.addWidget(self.bot_widget)

        self.retranslateUi(dialog)
        dialog.setAttribute(Qt.WA_DeleteOnClose)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("PreferenceShortcut", "Preference Shortcut"))
        self.title.setText(_translate("PreferenceShortcut", "Creating a new preference shortcut"))
        self.shortcut_label.setPlaceholderText(_translate("PreferenceShortcut", "i.e Mysql password"))
        self.data_type_label.setText(_translate("PreferenceShortcut", "Datatype:"))
        self.label_des.setText(_translate("PreferenceShortcut",
                                          "Label will be appeard in the expanding window to let you know the "
                                          "meaning of this preference"))
        self.type_label.setText(_translate("PreferenceShortcut", "Preference shortcut type:"))
        self.shortcut_for_des.setText(
            _translate("PreferenceShortcut", "This preference shortcut will be applied to the specified application"))
        self.shortcut_for_label.setText(_translate("PreferenceShortcut", "Preference shortcut for:"))
        self.label.setText(_translate("PreferenceShortcut", "Preference shortcut label:"))
        self.data_type_des.setText(_translate("PreferenceShortcut",
                                              "Type of the data, we will decide which kind of input element in "
                                              "the expanding window based on this information"))
        self.cancel_button.setText(_translate("PreferenceShortcut", "Cancel"))
        self.next_button.setText(_translate("PreferenceShortcut", "Next"))
