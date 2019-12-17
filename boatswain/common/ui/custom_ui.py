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

from typing import List

from PyQt5.QtCore import QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtWidgets import QSizePolicy, QWidget, QStyle, QToolButton, QLineEdit, QFileDialog, QItemDelegate, \
    QComboBox

from boatswain.common.services import system_service
from boatswain.resources_utils import getResource


class BQSizePolicy(QSizePolicy):
    def __init__(self, width=QSizePolicy.Preferred, height=QSizePolicy.Preferred, h_stretch=0, v_stretch=0):
        super().__init__(width, height)
        self.setHorizontalStretch(h_stretch)
        self.setVerticalStretch(v_stretch)


class ReloadableWidget:
    def reloadData(self):
        raise NotImplementedError()


class AutoResizeWidget(QWidget):
    def preferableSize(self) -> QSize:
        height = system_service.getScaleHeight() / 2
        width = height * 1.6
        return QSize(width, height)


class PathInputDelegate(QItemDelegate):

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):

        editor = ButtonLineEdit(getResource('resources/icons/folder.svg'), parent=parent)
        editor.setText(str(index.data()))
        editor.button_clicked.connect(lambda x: self.fileLooking(editor))
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(str(index.data()))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())

    def fileLooking(self, editor):
        file = str(QFileDialog.getExistingDirectory(self.parent(), "Select Directory"))
        if file:
            editor.setText(file)


class InputNumberDelegate(QItemDelegate):

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):

        editor = QLineEdit(parent)
        editor.setValidator(QIntValidator(0, 9999999))
        editor.setText(str(index.data()))
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(str(index.data()))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class ComboBoxDelegate(QItemDelegate):
    """ Combobox for QTableView
        Still have problem of overlapping with MacOS dark mode
    """

    def __init__(self, parent, values: List[str]):
        QItemDelegate.__init__(self, parent)
        self.values = values

    def createEditor(self, parent, option, index):

        editor = QComboBox(parent)
        editor.addItems(self.values)
        # editor.setCurrentIndex(self.values.index(index.data()))
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentIndex(self.values.index(index.data()))
        editor.blockSignals(False)

    def setModelData(self, editor: QComboBox, model, index):
        model.setData(index, editor.currentText())

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())


class ButtonLineEdit(QLineEdit):
    button_clicked = pyqtSignal(bool)

    def __init__(self, icon_file, parent=None):
        super(ButtonLineEdit, self).__init__(parent)

        self.button = QToolButton(self)
        self.button.setIcon(QIcon(icon_file))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(Qt.OpenHandCursor)
        self.button.clicked.connect(self.button_clicked.emit)

        self.setAttribute(Qt.WA_MacShowFocusRect, 0)

        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        button_size = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (button_size.width() + frame_width + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), button_size.width() + frame_width * 2 + 2),
                            max(self.minimumSizeHint().height(), button_size.height() + frame_width * 2 + 2))

    def resizeEvent(self, event):
        button_size = self.button.sizeHint()
        frame_width = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frame_width - button_size.width(),
                         (self.rect().bottom() - button_size.height() + 1) / 2)
        super(ButtonLineEdit, self).resizeEvent(event)
