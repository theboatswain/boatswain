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

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QTableView

from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.utils.custom_ui import BQSizePolicy
from boatswain.shortcut.create.preference_shortcut_creator import PreferencesShortcutCreator
from boatswain.shortcut.models.preferences_shortcut_model import PreferencesShortcutModel


class PreferencesShortcutWidget(object):

    def __init__(self, dialog, container: Container) -> None:
        self.container = container
        self.dialog = dialog
        self.setupUi(dialog)
        # dialog.setAttribute(Qt.WA_DeleteOnClose)

    def setupUi(self, dialog):
        dialog.resize(745, 314)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(745, 314))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.top_widget = QtWidgets.QWidget(dialog)
        self.top_widget.setSizePolicy(BQSizePolicy())
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.top_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.import_shortcut = QtWidgets.QPushButton(self.top_widget)
        self.import_shortcut.setObjectName("importShortcut")
        self.horizontalLayout.addWidget(self.import_shortcut)
        self.export_shortcut = QtWidgets.QPushButton(self.top_widget)
        self.export_shortcut.setObjectName("exportShortcut")
        self.horizontalLayout.addWidget(self.export_shortcut)
        self.hidden = QtWidgets.QWidget(self.top_widget)
        self.hidden.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontalLayout.addWidget(self.hidden)
        self.new_shortcut = QtWidgets.QPushButton(self.top_widget)
        self.new_shortcut.clicked.connect(self.onNewPortClicked)
        self.horizontalLayout.addWidget(self.new_shortcut)
        self.delete_shortcut = QtWidgets.QPushButton(self.top_widget)
        self.delete_shortcut.setObjectName("deleteShortcut")
        self.horizontalLayout.addWidget(self.delete_shortcut)
        self.verticalLayout.addWidget(self.top_widget)
        self.shortcut_table = QtWidgets.QTableView(dialog)
        self.verticalLayout.addWidget(self.shortcut_table)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)
        headers = ['label', 'default_value', 'pref_type', 'shortcut', 'mapping_to']
        display_headers = ['Label', 'Default value', 'Type', 'Shortcut', 'Mapping to']
        table_data = PreferencesShortcut.select().where(PreferencesShortcut.container == self.container)
        self.configureVolumeTable(self.shortcut_table, headers, display_headers, list(table_data), self.container)

    def retranslateUi(self, dialog: QDialog):
        _translate = QtCore.QCoreApplication.translate
        dialog.setWindowTitle(_translate("Shortcut", "Preferences shortcut") + " - " + self.container.name)
        self.import_shortcut.setText(_translate("Shortcut", "Import"))
        self.export_shortcut.setText(_translate("Shortcut", "Export"))
        self.new_shortcut.setText(_translate("Shortcut", "Add"))
        self.delete_shortcut.setText(_translate("Shortcut", "Delete"))

    def onNewPortClicked(self, checked):
        dialog = QDialog(self.dialog)
        dialog.ui = PreferencesShortcutCreator(dialog, self.container)
        dialog.exec_()

    def configureVolumeTable(self, tv: QTableView, header, display_header, data, container: Container):
        # set the table model
        table_model = PreferencesShortcutModel(data, header, display_header, container, self.dialog)
        tv.setModel(table_model)

        # hide grid
        tv.setShowGrid(False)

        # # set column width to fit contents
        # tv.resizeColumnsToContents()

        # # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        hh.setMinimumSectionSize(100)
        tv.resizeColumnsToContents()

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(True)

        tv.setSelectionBehavior(QAbstractItemView.SelectRows)
