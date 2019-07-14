from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, QItemSelectionModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView, QVBoxLayout, QWidget, QGridLayout, QLineEdit, QSizePolicy, \
    QLabel, QComboBox, QFrame, QHBoxLayout, QPushButton

from common.models.container import Container
from common.models.port_mapping import PortMapping
from common.utils.custom_ui import AutoResizeWidget, BQSizePolicy
from config.models.port_mapping_model import PortMappingModel


class PortMappingConfig(AutoResizeWidget):

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(11, 11, 11, 11)
        self.vertical_layout.setSpacing(6)
        self.top_widget = QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy())
        self.grid_layout = QGridLayout(self.top_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 12)
        self.grid_layout.setSpacing(6)
        self.ip_addr = QLineEdit(self.top_widget)
        self.ip_addr.setSizePolicy(BQSizePolicy(h_stretch=1, height=QSizePolicy.Fixed))
        self.ip_addr.setObjectName("ipAddr")
        self.ip_addr.setReadOnly(True)
        self.grid_layout.addWidget(self.ip_addr, 2, 1, 1, 1)
        self.ip_addr_label = QLabel(self.top_widget)
        self.grid_layout.addWidget(self.ip_addr_label, 2, 0, 1, 1)
        self.network_label = QLabel(self.top_widget)
        self.grid_layout.addWidget(self.network_label, 0, 0, 1, 1)
        self.network = QComboBox(self.top_widget)
        self.network.setObjectName("network")
        self.network.addItem("")
        self.grid_layout.addWidget(self.network, 0, 1, 1, 1)
        self.hidden_widget_2 = QWidget(self.top_widget)
        self.hidden_widget_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.grid_layout.addWidget(self.hidden_widget_2, 2, 2, 1, 1)
        self.vertical_layout.addWidget(self.top_widget)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.vertical_layout.addWidget(self.line)
        self.mid_widget = QWidget(self)
        self.mid_widget.setSizePolicy(BQSizePolicy())
        self.horizontal_layout = QHBoxLayout(self.mid_widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(6)
        self.port_label = QLabel(self.mid_widget)
        self.horizontal_layout.addWidget(self.port_label)
        self.hidden_widget = QWidget(self.mid_widget)
        self.hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.hidden_widget)
        self.new_port = QPushButton(self.mid_widget)
        self.new_port.setObjectName("newPort")
        self.horizontal_layout.addWidget(self.new_port)
        self.delete_port = QPushButton(self.mid_widget)
        self.delete_port.setObjectName("deletePort")
        self.horizontal_layout.addWidget(self.delete_port)
        self.vertical_layout.addWidget(self.mid_widget)
        self.port_mapping_table = QTableView(self)
        self.vertical_layout.addWidget(self.port_mapping_table)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        table_data = PortMapping.select().where(PortMapping.container == self.container)
        headers = ['targetPort', 'port', 'protocol', 'description']
        display_headers = ['Host Port', 'Container Port', 'Protocol', 'Description']
        self.configurePortTable(self.port_mapping_table, headers, display_headers, list(table_data), self.container)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.ip_addr_label.setText(_translate("PortMapping", "IP Address:"))
        self.network_label.setText(_translate("PortMapping", "Network:"))
        self.network.setItemText(0, _translate("PortMapping", "Default network"))
        self.port_label.setText(_translate("PortMapping", "Port mapping:"))
        self.new_port.setText(_translate("PortMapping", "New"))
        self.delete_port.setText(_translate("PortMapping", "Delete"))

    @pyqtSlot(bool, name='on_newPort_clicked')
    def onNewPortClicked(self, checked):
        self.port_mapping_table.model().addRecord(
            PortMapping(port=1000, targetPort=1000, description='description', container=self.container))
        self.port_mapping_table.resizeRowToContents(self.port_mapping_table.model().rowCount() - 1)
        flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        index = self.port_mapping_table.model().index(self.port_mapping_table.model().rowCount() - 1, 0)
        self.port_mapping_table.selectionModel().select(index, flags)

    @pyqtSlot(bool, name='on_deletePort_clicked')
    def onDeleteEnvClicked(self, checked):
        indicates = self.port_mapping_table.selectionModel().selectedRows()
        for item in sorted(indicates):
            self.port_mapping_table.model().removeRow(item.row())

    def configurePortTable(self, tv: QTableView, header, display_header, data, container: Container):
        # set the table model
        table_model = PortMappingModel(data, header, display_header, container, self)
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