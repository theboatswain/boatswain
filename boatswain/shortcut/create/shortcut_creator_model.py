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

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt

from boatswain.common.models.container import Container


class ShortcutCreatorModel(QAbstractTableModel):
    def __init__(self, data_in, header_data, display_header, container: Container, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.array_data = data_in
        self.header_data = header_data
        self.display_header = display_header
        self.container = container

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.array_data)

    def columnCount(self, parent=None, *args, **kwargs):
        if len(self.header_data) > 0:
            return len(self.header_data)
        return 0

    def data(self, index: QModelIndex, role=None):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole and role != Qt.EditRole:
            return QVariant()
        return QVariant(getattr(self.array_data[index.row()], self.header_data[index.column()]))

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.display_header[col].title())
        return QVariant()

    def sort(self, col, order=None):
        if order == Qt.DescendingOrder:
            self.array_data.sort(key=lambda x: getattr(x, self.header_data[col]), reverse=True)
        else:
            self.array_data.sort(key=lambda x: getattr(x, self.header_data[col]))
        self.layoutChanged.emit()

    def updateData(self, array_data):
        self.array_data = array_data
        self.layoutChanged.emit()

    def removeRow(self, p_int, parent=None, *args, **kwargs):
        if self.array_data[p_int].container is not None:
            self.array_data[p_int].delete_instance()
        self.array_data.pop(p_int)
        self.layoutChanged.emit()

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
