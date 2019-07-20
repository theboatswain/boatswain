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
from PyQt5.QtCore import QSize, QItemSelectionModel
from PyQt5.QtWidgets import QTableView, QAbstractItemView

from boatswain.common.models.container import Container
from boatswain.common.models.volume_mount import VolumeMount
from boatswain.common.utils.custom_ui import PathInputDelegate, ComboBoxDelegate
from boatswain.config.volume.volume_mount_config_ui import VolumeMountConfigUi
from boatswain.config.volume.volume_mount_config_model import VolumeMountModel


class VolumeMountConfig:
    _translate = QtCore.QCoreApplication.translate
    template = 'VolumeMountConfig'

    def preferableSize(self) -> QSize:
        return QSize(745, 354)

    def __init__(self, parent, container: Container) -> None:

        self.container = container
        self.ui = VolumeMountConfigUi(parent, container, self)
        self.retranslateUi()

        self.ui.new_mount.clicked.connect(self.onNewMountClicked)
        self.ui.delete_mount.clicked.connect(self.onDeleteMountClicked)

        table_data = VolumeMount.select().where(VolumeMount.container == self.container)
        headers = ['host_path', 'mode', 'container_path']
        display_headers = ['Host Path', 'Mode', 'Container Path']
        self.configureVolumeTable(self.ui.mount_table, headers, display_headers, list(table_data), self.container)
        self.ui.mount_table.setItemDelegateForColumn(0, PathInputDelegate(self.ui.mount_table))
        modes = ['rw', 'ro']
        self.ui.mount_table.setItemDelegateForColumn(1, ComboBoxDelegate(self.ui.mount_table, modes))

    def retranslateUi(self):
        self.ui.volume_label.setText(self._translate(self.template, "Volume mounts:"))
        self.ui.new_mount.setText(self._translate(self.template, "Add"))
        self.ui.delete_mount.setText(self._translate(self.template, "Delete"))

    def onNewMountClicked(self):
        self.ui.mount_table.model().addRecord(
            VolumeMount(host_path='/tmp', container_path='/tmp', description='description', container=self.container))
        self.ui.mount_table.resizeRowToContents(self.ui.mount_table.model().rowCount() - 1)
        flags = QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows
        index = self.ui.mount_table.model().index(self.ui.mount_table.model().rowCount() - 1, 0)
        self.ui.mount_table.selectionModel().select(index, flags)
        # Todo: Prevent Duplicate mount point exception

    def onDeleteMountClicked(self):
        indicates = self.ui.mount_table.selectionModel().selectedRows()
        for item in sorted(indicates):
            self.ui.mount_table.model().removeRow(item.row())

    def configureVolumeTable(self, tv: QTableView, header, display_header, data, container: Container):
        # set the table model
        table_model = VolumeMountModel(data, header, display_header, container, self.ui)
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
