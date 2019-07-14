from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QVariant
from PyQt5.QtCore import Qt

from common.models.container import Container


class PortMappingModel(QAbstractTableModel):
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

    def setData(self, index, value, role=Qt.EditRole):
        if role == Qt.EditRole:
            setattr(self.array_data[index.row()], self.header_data[index.column()], value)
            self.array_data[index.row()].save()
            container = self.array_data[index.row()].container
            if container is not None:
                # Todo: Clean up the previous container
                self.container.container_id = ""
                self.container.save()
            return True
        else:
            return False

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

    def addRecord(self, record):
        self.array_data.append(record)
        self.layoutChanged.emit()

    def removeRow(self, p_int, parent=None, *args, **kwargs):
        if self.array_data[p_int].container is not None:
            self.array_data[p_int].delete_instance()
            # Todo: Clean up the previous container
            self.container.container_id = ""
            self.container.save()
        self.array_data.pop(p_int)
        self.layoutChanged.emit()

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
