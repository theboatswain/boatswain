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
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QTableView, QHeaderView, QFileDialog

from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.services import containers_service, config_service, shortcut_service
from boatswain.common.services.system_service import rt
from boatswain.common.shortcut.shortcut_yaml import ShortcutYaml
from boatswain.common.ui.switch import SwitchBox
from boatswain.common.utils import message_utils
from boatswain.common.utils.constants import SHORTCUT_CONF_CHANGED_CHANNEL, CONTAINER_CONF_CHANGED
from boatswain.shortcut.create.shortcut_creator import ShortcutCreator
from boatswain.shortcut.preferences_shortcut_config_model import ShortcutCreatorModel
from boatswain.shortcut.preferences_shortcut_config_ui import PreferencesShortcutConfigUi


class PreferencesShortcutConfig(object):
    _tr = QtCore.QCoreApplication.translate
    template = 'PreferencesShortcutConfig'
    DOWN = 1
    UP = -1

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.dialog = QDialog(parent)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.ui = PreferencesShortcutConfigUi(self.dialog, container, self)
        self.dialog.ui = self.ui
        self.ui.new_shortcut.clicked.connect(self.onNewShortcutClicked)
        self.ui.delete_shortcut.clicked.connect(self.onDeleteShortcutClicked)

        self.retranslateUi()
        headers = ['label', 'default_value', 'pref_type', 'shortcut', 'mapping_to', 'enabled']
        display_headers = ['Label', 'Default value', 'Type', 'Shortcut', 'Mapping to', 'Enabled']
        table_data = list(shortcut_service.getShortcuts(self.container))
        self.table_model = ShortcutCreatorModel(table_data, headers, display_headers, container, self.dialog)
        self.configurePreferenceTable(self.ui.shortcut_table, self.table_model)
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.ui.shortcut_table.doubleClicked.connect(self.onDoubleClickItem)
        self.ui.move_up.clicked.connect(lambda x: self.moveCurrentRow(self.UP))
        self.ui.move_down.clicked.connect(lambda x: self.moveCurrentRow(self.DOWN))
        self.drawSwitches(table_data)
        self.ui.export_shortcut.clicked.connect(self.export)
        self.ui.import_shortcut.clicked.connect(self.importFromYaml)

    def retranslateUi(self):
        self.dialog.setWindowTitle(self._tr(self.template, "Preferences shortcut") + " - " + self.container.name)
        self.ui.import_shortcut.setText(self._tr(self.template, "Import"))
        self.ui.export_shortcut.setText(self._tr(self.template, "Export"))
        self.ui.new_shortcut.setText(self._tr(self.template, "+"))
        self.ui.delete_shortcut.setText(self._tr(self.template, "-"))
        self.ui.move_up.setText(self._tr(self.template, "↑"))
        self.ui.move_down.setText(self._tr(self.template, "↓"))

    def drawSwitches(self, table_data):
        for i, record in enumerate(table_data):
            index = self.table_model.index(i, 5)
            switch = SwitchBox(self.ui.shortcut_table, record.enabled, record)
            self.ui.shortcut_table.setIndexWidget(index, switch)

    def onNewShortcutClicked(self):
        shortcut = PreferencesShortcut()
        shortcut_creator = ShortcutCreator(self.container, self.dialog, shortcut)
        if shortcut_creator.show():
            self.reloadData()

    def onDeleteShortcutClicked(self):
        indicates = self.ui.shortcut_table.selectionModel().selectedRows()
        for item in sorted(indicates, reverse=True):
            self.ui.shortcut_table.model().removeRow(item.row())
        self.ui.shortcut_table.resizeRowsToContents()
        containers_service.fire(self.container, SHORTCUT_CONF_CHANGED_CHANNEL)
        config_service.setAppConf(self.container, CONTAINER_CONF_CHANGED, 'true')

    def onDoubleClickItem(self, index: QModelIndex):
        data = self.table_model.array_data[index.row()]
        shortcut_creator = ShortcutCreator(self.container, self.dialog, data)
        if shortcut_creator.show():
            self.reloadData()

    def moveCurrentRow(self, direction=DOWN):
        if direction not in (self.DOWN, self.UP):
            return

        model = self.table_model
        sel_model = self.ui.shortcut_table.selectionModel()
        selected = sel_model.selectedRows()
        if not selected:
            return

        indexes = sorted(selected, key=lambda x: x.row(), reverse=(direction == self.DOWN))

        for idx in indexes:
            row_num = idx.row()
            new_row = row_num + direction
            if not (0 <= new_row < model.rowCount()):
                continue

            row_item = model.array_data[row_num]
            row_item.order = model.array_data[new_row].order + direction
            row_item.save()
        self.reloadData()

    def reloadData(self):
        table_data = list(shortcut_service.getShortcuts(self.container))
        self.table_model.updateData(list(table_data))
        self.ui.shortcut_table.resizeRowsToContents()
        self.drawSwitches(table_data)
        containers_service.fire(self.container, SHORTCUT_CONF_CHANGED_CHANNEL)

    def show(self):
        self.dialog.exec_()

    def export(self):
        if self.table_model.rowCount() < 1:
            message_utils.error("Unable to export", "Nothing to export")
            return
        shortcut_yaml = ShortcutYaml.build(self.container)
        name = QFileDialog.getSaveFileName(self.dialog, 'Export Preference shortcuts',
                                           directory="%s.yaml" % shortcut_yaml.image_name, filter="YAML (*.yaml)")
        if name[0]:
            with open(name[0], 'w') as file:
                file.write(shortcut_yaml.toYAML())

    def importFromYaml(self):
        fname = QFileDialog.getOpenFileName(self.dialog, 'Open YAML file', filter="YAML (*.yaml)")
        if fname[0]:
            with open(fname[0], 'r') as content_file:
                content = content_file.read()
            shortcut_yaml = ShortcutYaml.fromYaml(content)
            if shortcut_yaml.image_name == self.container.image_name:
                shortcut_service.importShortcuts(self.container, shortcut_yaml.shortcuts)
                self.reloadData()
            else:
                message_utils.error("Unable to import", "The import file is not designed for this app")

    def configurePreferenceTable(self, tv: QTableView, table_model):
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
        hh: QHeaderView = tv.horizontalHeader()
        hh.setSectionResizeMode(1, QHeaderView.Stretch)
        hh.setMinimumSectionSize(rt(60))
        tv.resizeColumnsToContents()

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(False)

        tv.setSelectionBehavior(QAbstractItemView.SelectRows)
