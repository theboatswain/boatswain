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

from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt, pyqtSignal, pyqtSlot, QEvent, QPropertyAnimation
from PyQt5.QtGui import QIcon, QIntValidator, QPixmap, QResizeEvent
from PyQt5.QtWidgets import QSizePolicy, QWidget, QStyle, QToolButton, QLineEdit, QFileDialog, QItemDelegate, \
    QComboBox, QLabel, QScrollArea, QFrame

from boatswain.common.services import system_service
from boatswain.common.utils import utils


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
        height = system_service.screen_height / 2
        width = height * 1.6
        return QSize(width, height)


class PathInputDelegate(QItemDelegate):

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):

        editor = ButtonLineEdit(':/icons/folder.svg', parent=parent)
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


class FolderIcon(QWidget):
    def __init__(self, parent: QWidget, label_text: str):
        super().__init__(parent)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(2)
        self.icon = QLabel(self)
        self.icon.setPixmap(QPixmap(':/icons/folder.svg').scaled(QSize(16, 16), Qt.KeepAspectRatio))
        self.horizontal_layout.addWidget(self.icon)
        self.label = QLabel(self)
        self.label.setText(label_text)
        # font = QtGui.QFont()
        # font.setPointSize(11)
        # self.label.setFont(font)
        self.current_label_visible = True
        self.horizontal_layout.addWidget(self.label)

    def predictWidth(self):
        label_size = self.label.maximumWidth() if self.label.maximumWidth() == 0 else self.label.sizeHint().width()
        return self.icon.sizeHint().width() + 2 + label_size

    def enterEvent(self, event: QEvent):
        if self.label.maximumWidth() == 0:
            self.current_label_visible = False
            self.animation = QPropertyAnimation(self.label, b"maximumWidth")
            self.animation.setDuration(150)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.label.sizeHint().width())
            self.animation.start()

    def leaveEvent(self, event: QEvent):
        if not self.current_label_visible:
            self.animation = QPropertyAnimation(self.label, b"maximumWidth")
            self.animation.setDuration(150)
            self.animation.setStartValue(self.label.sizeHint().width())
            self.animation.setEndValue(0)
            self.animation.start()
            self.current_label_visible = True


class PathViewWidget(QWidget):

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(3, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setStyleSheet('QScrollBar {width:0px;}')
        self.scroll_area.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)

        self.app_list = QWidget(self)
        self.app_list.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.app_list)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(0)
        self.horizontal_layout.setAlignment(Qt.AlignLeft)
        self.app_list.setLayout(self.horizontal_layout)
        self.scroll_area.setWidget(self.app_list)

        self.main_layout.addWidget(self.scroll_area)

        self.labels = []
        self.current_width = 0

    def setPath(self, path):
        self.clearPath()
        self.path = path
        self.labels.clear()
        parts = utils.split_all(path)
        for index, part in enumerate(parts):
            if part == '/':
                continue

            label = FolderIcon(self, part)
            label.label.setMaximumWidth(0)
            self.horizontal_layout.addWidget(label)
            self.labels.append(label)
            if index < len(parts) - 1:
                separator = QLabel()
                separator.setText(' > ')
                self.horizontal_layout.addWidget(separator)

    def clearPath(self):
        while self.horizontal_layout.count():
            item = self.horizontal_layout.takeAt(0)
            item.widget().deleteLater()

    def calculateCurrentWidth(self):
        current_width = 0
        for label in self.labels:
            current_width += label.predictWidth()
        return current_width

    def resizePaths(self):
        i = len(self.labels) - 1
        while self.calculateCurrentWidth() < self.max_width - 50 and i >= 0:
            self.labels[i].label.setMaximumWidth(999)
            i -= 1

        j = 0
        while self.calculateCurrentWidth() > self.max_width - 50 and j < len(self.labels):
            self.labels[j].label.setMaximumWidth(0)
            j += 1

    def resizeEvent(self, event: QResizeEvent):
        self.max_width = event.size().width()
        self.resizePaths()
        QWidget.resizeEvent(self, event)


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
