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

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QTableView

from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.services import containers_service, config_service
from boatswain.common.utils.constants import SHORTCUT_CONF_CHANGED_CHANNEL, CONTAINER_CONF_CHANGED
from boatswain.shortcut.create.shortcut_creator import ShortcutCreator
from boatswain.shortcut.create.shortcut_creator_model import ShortcutCreatorModel
from boatswain.shortcut.preferences_shortcut_config_ui import PreferencesShortcutConfigUi


class PreferencesShortcutConfig(object):
    _translate = QtCore.QCoreApplication.translate
    template = 'PreferencesShortcutConfig'

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.dialog = QDialog(parent)
        self.ui = PreferencesShortcutConfigUi(self.dialog, container, self)
        self.dialog.ui = self.ui
        self.ui.new_shortcut.clicked.connect(self.onNewShortcutClicked)
        self.ui.delete_shortcut.clicked.connect(self.onDeleteShortcutClicked)

        self.retranslateUi()
        headers = ['label', 'default_value', 'pref_type', 'shortcut', 'mapping_to']
        display_headers = ['Label', 'Default value', 'Type', 'Shortcut', 'Mapping to']
        table_data = PreferencesShortcut.select().where(PreferencesShortcut.container == self.container)
        self.table_model = ShortcutCreatorModel(list(table_data), headers, display_headers, container, self.dialog)
        self.configureVolumeTable(self.ui.shortcut_table, self.table_model)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.ui.shortcut_table.doubleClicked.connect(self.onDoubleClickItem)

    def retranslateUi(self):
        self.dialog.setWindowTitle(self._translate(self.template, "Preferences shortcut") + " - " + self.container.name)
        self.ui.import_shortcut.setText(self._translate(self.template, "Import"))
        self.ui.export_shortcut.setText(self._translate(self.template, "Export"))
        self.ui.new_shortcut.setText(self._translate(self.template, "Add"))
        self.ui.delete_shortcut.setText(self._translate(self.template, "Delete"))

    def onNewShortcutClicked(self):
        shortcut = PreferencesShortcut()
        shortcut_creator = ShortcutCreator(self.container, self.dialog, shortcut)
        if shortcut_creator.show():
            table_data = PreferencesShortcut.select().where(PreferencesShortcut.container == self.container)
            self.table_model.updateData(list(table_data))
            self.ui.shortcut_table.resizeRowsToContents()

    def onDeleteShortcutClicked(self):
        indicates = self.ui.shortcut_table.selectionModel().selectedRows()
        for item in sorted(indicates, reverse=True):
            self.ui.shortcut_table.model().removeRow(item.row())
        self.ui.shortcut_table.resizeRowsToContents()
        containers_service.fire(self.container, SHORTCUT_CONF_CHANGED_CHANNEL, True)
        config_service.setAppConf(self.container, CONTAINER_CONF_CHANGED, 'true')

    def onDoubleClickItem(self, index: QModelIndex):
        data = self.table_model.array_data[index.row()]
        shortcut_creator = ShortcutCreator(self.container, self.dialog, data)
        if shortcut_creator.show():
            table_data = PreferencesShortcut.select().where(PreferencesShortcut.container == self.container)
            self.table_model.updateData(list(table_data))
            self.ui.shortcut_table.resizeRowsToContents()

    def show(self):
        self.dialog.exec_()

    def configureVolumeTable(self, tv: QTableView, table_model):
        # set the table model

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
