from PyQt5 import QtCore
from PyQt5.QtCore import QMetaObject, QSize, pyqtSlot, QItemSelectionModel
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QTableView, QAbstractItemView
from common.models.container import Container
from common.models.volume_mount import VolumeMount
from common.utils.custom_ui import AutoResizeWidget, BQSizePolicy, PathInputDelegate
from config.models.volume_mount_model import VolumeMountModel


class VolumeMountConfig(AutoResizeWidget):

    def preferableSize(self) -> QSize:
        return QSize(745, 314)

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.top_widget = QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy())
        self.horizontalLayout = QHBoxLayout(self.top_widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.volume_label = QLabel(self.top_widget)
        self.horizontalLayout.addWidget(self.volume_label)
        self.hidden_widget = QWidget(self.top_widget)
        self.hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontalLayout.addWidget(self.hidden_widget)
        self.new_mount = QPushButton(self.top_widget)
        self.new_mount.setObjectName("newMount")
        self.horizontalLayout.addWidget(self.new_mount)
        self.delete_mount = QPushButton(self.top_widget)
        self.delete_mount.setObjectName("deleteMount")
        self.horizontalLayout.addWidget(self.delete_mount)
        self.verticalLayout.addWidget(self.top_widget)
        self.volume_mount_table = QTableView(self)
        self.verticalLayout.addWidget(self.volume_mount_table)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)
        table_data = VolumeMount.select().where(VolumeMount.container == self.container)
        headers = ['host_path', 'mode', 'container_path']
        display_headers = ['Host Path', 'Mode', 'Container Path']
        self.configureVolumeTable(self.volume_mount_table, headers, display_headers, list(table_data), self.container)
        self.volume_mount_table.setItemDelegateForColumn(0, PathInputDelegate(self.volume_mount_table))

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.volume_label.setText(_translate("MainWindow", "Volume mounts:"))
        self.new_mount.setText(_translate("MainWindow", "New"))
        self.delete_mount.setText(_translate("MainWindow", "Delete"))

    @pyqtSlot(bool, name='on_newMount_clicked')
    def onNewPortClicked(self, checked):
        self.volume_mount_table.model().addRecord(
            VolumeMount(host_path='/tmp', container_path='/tmp', description='description', container=self.container))
        self.volume_mount_table.resizeRowToContents(self.volume_mount_table.model().rowCount() - 1)
        flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        index = self.volume_mount_table.model().index(self.volume_mount_table.model().rowCount() - 1, 0)
        self.volume_mount_table.selectionModel().select(index, flags)

    @pyqtSlot(bool, name='on_deleteMount_clicked')
    def onDeleteEnvClicked(self, checked):
        indicates = self.volume_mount_table.selectionModel().selectedRows()
        for item in sorted(indicates):
            self.volume_mount_table.model().removeRow(item.row())

    def configureVolumeTable(self, tv: QTableView, header, display_header, data, container: Container):
        # set the table model
        table_model = VolumeMountModel(data, header, display_header, container, self)
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
        hh.resizeSection(0, 350)
        hh.resizeSection(1, 50)


        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(True)

        tv.setSelectionBehavior(QAbstractItemView.SelectRows)