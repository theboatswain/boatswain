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

from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt


class LoggingMonitorModel(QAbstractTableModel):
    def __init__(self, data_in, header_data, display_header, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.array_data = data_in
        self.header_data = header_data
        self.display_header = display_header
        self.stop_showing = False
        self.non_showing_data = []

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
        return QVariant(str(self.array_data[index.row()][self.header_data[index.column()]]))

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.display_header[col].title())
        return QVariant()

    def insertRows(self, position: int, count: int, rows=None, parent=None, *args, **kwargs):
        if rows is None:
            return False
        if not self.stop_showing:
            self.beginInsertRows(parent, position, position + count - 1)
            self.array_data += rows
            self.endInsertRows()
        else:
            self.non_showing_data += rows
        return True

    def stopShowing(self):
        self.stop_showing = True

    def reShowing(self):
        if len(self.non_showing_data) > 0:
            parent = self.index(self.rowCount(), 0)
            self.beginInsertRows(parent, self.rowCount(), len(self.non_showing_data) + self.rowCount() - 1)
            self.array_data += self.non_showing_data
            self.endInsertRows()
            self.stop_showing = False
            self.non_showing_data.clear()

    def cleanRows(self):
        parent = self.index(self.rowCount(), 0)
        self.beginRemoveRows(parent, 0, self.rowCount())
        self.array_data = []
        self.endRemoveRows()

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
