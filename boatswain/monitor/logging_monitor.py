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

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QObject, QItemSelection, QSortFilterProxyModel, QRegExp
from PyQt5.QtWidgets import QDialog, QAbstractItemView, QTableView, QHeaderView
from docker.types import CancellableStream

from boatswain.common.models.container import Container
from boatswain.common.services import containers_service
from boatswain.common.services.system_service import applyFontRatio, rt
from boatswain.common.services.worker_service import Worker, threadpool
from boatswain.monitor.logging_monitor_model import LoggingMonitorModel
from boatswain.monitor.logging_monitor_ui import LoggingMonitorUi


class LoggingMonitor(QObject):
    logs: CancellableStream

    def __init__(self, container: Container) -> None:
        super().__init__()
        self.dialog = QDialog()
        self.dialog.setWindowTitle(container.name + self.tr("'s logs"))
        self.dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.dialog.closeEvent = self.onCloseDialog
        self.ui = LoggingMonitorUi(self.dialog)
        self.dialog.ui = self.ui
        self.container = container
        self.ui.now.clicked.connect(self.onNowActivate)

        headers = ['Date', 'Time', 'Message']
        self.table_model = LoggingMonitorModel([], headers, headers, self.dialog)
        self.proxy_model = QSortFilterProxyModel(self.dialog)
        self.proxy_model.setSourceModel(self.table_model)
        self.configurePreferenceTable(self.ui.log_list_table, self.proxy_model)
        self.proxy_model.rowsInserted.connect(self.rowsInserted)
        worker = Worker(self.streamLogs)
        threadpool.start(worker)

        self.ui.clear.clicked.connect(self.onCleanLogs)
        self.ui.reload.clicked.connect(self.onReload)
        self.ui.info.clicked.connect(self.infoClicked)

        selection_model = self.ui.log_list_table.selectionModel()
        selection_model.selectionChanged.connect(self.updateLogDetails)
        self.ui.search.returnPressed.connect(self.find)
        self.dialog.closeEvent = self.closeEvent

    def show(self):
        self.dialog.show()

    def rowsInserted(self, parent, start, end):
        self.ui.log_list_table.scrollToBottom()

    def streamLogs(self):
        self.logs = containers_service.streamLogs(self.container)
        if self.logs:
            for log in self.logs:
                res = log.decode("utf-8")
                parts = res.split('Z', 1)
                timestr = parts[0].split('T')
                date = timestr[0]
                time = timestr[1][0:12]
                message = parts[1].strip()
                if not message:
                    continue
                position = self.table_model.rowCount()
                parent = self.table_model.index(position, 0)
                self.table_model.insertRows(position, 1, rows=[{'Date': date, 'Time': time, 'Message': message}],
                                            parent=parent)
                self.ui.log_list_table.resizeRowToContents(position)

    def onCloseDialog(self, event):
        self.logs.close()
        QDialog.closeEvent(self.dialog, event)

    def onCleanLogs(self):
        self.table_model.cleanRows()

    def onReload(self):
        self.logs.close()
        self.onCleanLogs()
        worker = Worker(self.streamLogs)
        threadpool.start(worker)

    def onNowActivate(self, checked: bool):
        if checked:
            self.table_model.reShowing()
        else:
            self.table_model.stopShowing()

    def updateLogDetails(self, selected: QItemSelection, deselected: QItemSelection):
        for index in selected.indexes():
            if index.column() == 0:
                actual_index = self.proxy_model.mapToSource(index)
                data = self.table_model.array_data[actual_index.row()]
                self.ui.log_details_label.setHtml(data['Message'])
                break

    def find(self, column=2):
        text = self.ui.search.text()
        self.proxy_model.setFilterRegExp(QRegExp(text, Qt.CaseSensitive, QRegExp.FixedString))
        self.proxy_model.setFilterKeyColumn(column)

    def infoClicked(self, checked):
        if checked:
            self.ui.log_details.show()
        else:
            self.ui.log_details.hide()

    def closeEvent(self, event):
        self.logs.close()
        QDialog.closeEvent(self.dialog, event)

    def configurePreferenceTable(self, tv: QTableView, table_model):
        # set the table model

        tv.setModel(table_model)

        # hide grid
        tv.setShowGrid(False)

        tv.setAlternatingRowColors(True)
        # # set column width to fit contents
        # tv.resizeColumnsToContents()

        # # hide vertical header
        vh = tv.verticalHeader()
        vh.setDefaultSectionSize(rt(5))
        vh.setVisible(False)

        # set horizontal header properties
        hh: QHeaderView = tv.horizontalHeader()
        hh.setStretchLastSection(True)
        hh.setMinimumSectionSize(rt(110))
        font = QtGui.QFont()
        font.setPointSize(applyFontRatio(10))
        hh.setFont(font)
        tv.resizeColumnsToContents()

        font = QtGui.QFont()
        font.setPointSize(applyFontRatio(12))
        tv.setFont(font)

        # set row height
        tv.resizeRowsToContents()

        # enable sorting
        tv.setSortingEnabled(False)

        tv.setSelectionBehavior(QAbstractItemView.SelectRows)
