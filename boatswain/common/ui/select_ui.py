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

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QWidget, QPushButton, QMenu

from boatswain.common.services.system_service import rt


class SelectUi(QPushButton):
    current_option: str
    on_option_selected = pyqtSignal(str)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.options = {}
        self.setFlat(True)
        padding = "%dpx %dpx %dpx %dpx" % (rt(1), rt(7), rt(1), rt(10))
        self.setStyleSheet("border: 1px solid #999999; padding: %s; border-radius: 2px" % padding)
        self.mouseReleaseEvent = self.onSelectClicked

    def addItem(self, option: str, label: str = None, separate_before: bool = False, separate_after: bool = False,
                handler=None):
        if label is None:
            label = option
        self.options[option] = {'label': label, 'separate_after': separate_after, 'key': option,
                                'separate_before': separate_before, 'handler': handler}
        if len(self.options) == 1:
            self.setCurrentOption(option)

    def setCurrentOption(self, option):
        self.current_option = option
        self.setText(option + ' ▿')

    def onSelectClicked(self, event: QMouseEvent):
        menu = QMenu(self.parentWidget())
        for item in self.options:
            if self.options[item]['separate_before']:
                menu.addSeparator()
            menu.addAction(self.options[item]['label'])
            if self.options[item]['separate_after']:
                menu.addSeparator()

        menu.triggered.connect(self.onSelection)
        menu.exec_(self.mapToGlobal(event.pos()))

    def onSelection(self, action):
        option = {}
        for opt in self.options:
            if self.options[opt]['label'] == action.text():
                option = self.options[opt]
        if option['handler'] is not None:
            option['handler']()
        else:
            self.setCurrentOption(option['key'])
            self.on_option_selected.emit(option['key'])

    def getCurrentOption(self):
        return self.current_option

    def clear(self):
        to_be_deleted = []
        for opt in self.options:
            to_be_deleted.append(opt)
        for opt in to_be_deleted:
            self.options.pop(opt, None)
