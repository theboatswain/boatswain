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
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPainter, QPen, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QPushButton, QMenu, QAction, QComboBox

from boatswain.common.services import global_preference_service
from boatswain.common.services.system_service import rt


class MultiLevelSelectionUi(QPushButton):
    current_option: str
    on_option_selected = pyqtSignal(str)
    currentTextChanged = pyqtSignal(str)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.options = {}
        self.menues = []
        self.setFlat(True)
        padding = "%dpx %dpx %dpx %dpx" % (rt(1), rt(7), rt(1), rt(10))
        self.setProperty('class', 'border-button')
        self.setStyleSheet("padding: %s; Text-align:left" % padding)
        self.mouseReleaseEvent = self.onSelectClicked

    def setData(self, options: dict):
        self.options = options

    def setCurrentOption(self, option):
        self.current_option = option
        # self.setText(self.options[option]['small_label'] + '    ')

    def setCurrentText(self, text):
        self.setCurrentOption(text)

    def createMenu(self, options, name=None):
        menu = QMenu(name, None)
        self.menues.append(menu)
        for key in options:
            menu.addSeparator()
            if options[key] == 1:
                menu.addAction(key)
            else:
                menu.addMenu(self.createMenu(options[key], key))
        return menu

    def onSelectClicked(self, event: QMouseEvent):
        menu = self.createMenu(self.options)

        menu.triggered.connect(self.onSelection)
        menu.exec_(self.mapToGlobal(event.pos()))

    def onSelection(self, action: QAction):
        option = {}
        for opt in self.options:
            if opt == action.data():
                option = self.options[opt]
        if option['handler'] is not None:
            option['handler']()
        else:
            self.setCurrentOption(option['key'])
            self.on_option_selected.emit(str(option['key']))
            self.currentTextChanged.emit(str(option['key']))

    def getCurrentOption(self):
        return self.current_option

    def paintEvent(self, event: QtGui.QPaintEvent):
        QPushButton.paintEvent(self, event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        color = global_preference_service.getInMemoryPreferences("@selection_color")
        painter.setPen(QPen(QBrush(QColor(color)), 1))
        painter.setBrush(QBrush(QColor(color)))
        painter.drawLine(self.width() - rt(17), rt(8), self.width() - rt(12), rt(13))
        painter.drawLine(self.width() - rt(12), rt(13), self.width() - rt(7), rt(8))


class SelectUi(QPushButton):
    current_option: str
    on_option_selected = pyqtSignal(str)
    currentTextChanged = pyqtSignal(str)
    currentIndexChanged = pyqtSignal(int)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.options = {}
        self.index = []
        self.setFlat(True)
        padding = "%dpx %dpx %dpx %dpx" % (rt(1), rt(7), rt(1), rt(10))
        self.setProperty('class', 'border-button')
        self.setStyleSheet("padding: %s; Text-align:left" % padding)
        self.mouseReleaseEvent = self.onSelectClicked

    def addItem(self, key: str, small_label: str = None, label: str = None, separate_before: bool = False,
                separate_after: bool = False, handler=None):
        if small_label is None:
            small_label = key
        if label is None:
            label = small_label
        self.options[key] = {'label': label, 'separate_after': separate_after, 'key': key, 'small_label': small_label,
                             'separate_before': separate_before, 'handler': handler}
        self.index.append(self.options[key])
        self.options[key]['index'] = len(self.index) - 1
        if len(self.options) == 1:
            self.setCurrentOption(key)

    def setCurrentOption(self, option):
        self.current_option = option
        self.setText(self.options[option]['small_label'] + '    ')

    def setCurrentIndex(self, index):
        option = self.index[index]
        self.setCurrentOption(option['key'])

    def setCurrentText(self, text):
        self.setCurrentOption(text)

    def onSelectClicked(self, event: QMouseEvent):
        menu = QMenu(None)
        for key in self.options:
            if self.options[key]['separate_before']:
                menu.addSeparator()
            action = menu.addAction(self.options[key]['label'])
            action.setData(key)
            if self.options[key]['separate_after']:
                menu.addSeparator()

        menu.triggered.connect(self.onSelection)
        menu.exec_(self.mapToGlobal(event.pos()))

    def onSelection(self, action: QAction):
        option = {}
        for opt in self.options:
            if opt == action.data():
                option = self.options[opt]
        if option['handler'] is not None:
            option['handler']()
        else:
            self.setCurrentOption(option['key'])
            self.on_option_selected.emit(str(option['key']))
            self.currentTextChanged.emit(str(option['key']))
            self.currentIndexChanged.emit(option['index'])

    def getCurrentOption(self):
        return self.current_option

    def clear(self):
        to_be_deleted = []
        for opt in self.options:
            to_be_deleted.append(opt)
        for opt in to_be_deleted:
            self.options.pop(opt, None)

    def paintEvent(self, event: QtGui.QPaintEvent):
        QPushButton.paintEvent(self, event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.HighQualityAntialiasing)
        color = global_preference_service.getInMemoryPreferences("@selection_color")
        painter.setPen(QPen(QBrush(QColor(color)), 1))
        painter.setBrush(QBrush(QColor(color)))
        painter.drawLine(self.width() - rt(17), rt(8), self.width() - rt(12), rt(13))
        painter.drawLine(self.width() - rt(12), rt(13), self.width() - rt(7), rt(8))
