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

from PyQt5 import QtCore
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView
from boatswain.common.services import port_mapping_service

from boatswain.common.models.container import Container
from boatswain.common.models.port_mapping import PortMapping
from boatswain.common.ui.custom_ui import ComboBoxDelegate, InputNumberDelegate
from boatswain.config.port.port_mapping_config_model import PortMappingModel
from boatswain.config.port.port_mapping_config_ui import PortMappingConfigUi


class PortMappingConfig:
    _translate = QtCore.QCoreApplication.translate
    template = 'PortMappingConfig'

    networks = ['Default network']

    def __init__(self, parent, container: Container) -> None:
        self.ui = PortMappingConfigUi(parent, container, self)
        self.container = container

        for network in self.networks:
            self.ui.network.addItem(self._translate(self.template, network))
        self.retranslateUi()

        self.ui.new_port.clicked.connect(self.onNewPortClicked)
        self.ui.delete_port.clicked.connect(self.onDeletePortClicked)

        table_data = port_mapping_service.getPortMappings(self.container)
        headers = ['target_port', 'port', 'protocol', 'description']
        display_headers = ['Host Port', 'Container Port', 'Protocol', 'Description']
        self.configurePortTable(self.ui.mapping_table, headers, display_headers, list(table_data), container)
        protocols = ['tcp', 'udp']
        self.ui.mapping_table.setItemDelegateForColumn(2, ComboBoxDelegate(self.ui.mapping_table, protocols))
        self.ui.mapping_table.setItemDelegateForColumn(1, InputNumberDelegate(self.ui.mapping_table))
        self.ui.mapping_table.setItemDelegateForColumn(0, InputNumberDelegate(self.ui.mapping_table))

    def retranslateUi(self):
        self.ui.ip_addr_label.setText(self._translate(self.template, "IP Address:"))
        self.ui.network_label.setText(self._translate(self.template, "Network:"))
        self.ui.port_label.setText(self._translate("PortMapping", "Port mapping:"))
        self.ui.new_port.setText(self._translate("PortMapping", "Add"))
        self.ui.delete_port.setText(self._translate("PortMapping", "Delete"))

    def onNewPortClicked(self):
        self.ui.mapping_table.model().addRecord(
            PortMapping(port=1000, target_port=1000, description='description', container=self.container))
        flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        index = self.ui.mapping_table.model().index(self.ui.mapping_table.model().rowCount() - 1, 0)
        self.ui.mapping_table.selectionModel().select(index, flags)
        self.ui.mapping_table.resizeRowsToContents()

    def onDeletePortClicked(self):
        indicates = self.ui.mapping_table.selectionModel().selectedRows()
        for item in sorted(indicates, reverse=True):
            self.ui.mapping_table.model().removeRow(item.row())
        self.ui.mapping_table.resizeRowsToContents()

    def configurePortTable(self, tv: QTableView, header, display_header, data, container: Container):
        # set the table model
        table_model = PortMappingModel(data, header, display_header, container, self.ui)
        tv.setModel(table_model)

        # hide grid
        tv.setShowGrid(False)

        # # hide vertical header
        vh = tv.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        hh.setMinimumSectionSize(100)

        # set column width to fit contents
        tv.resizeColumnsToContents()

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(True)

        tv.setSelectionBehavior(QAbstractItemView.SelectRows)
