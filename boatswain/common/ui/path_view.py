from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QSize, QEvent, QPropertyAnimation, Qt
from PyQt5.QtGui import QIcon, QResizeEvent
from PyQt5.QtWidgets import QWidget, QLabel, QScrollArea, QFrame, QSizePolicy

from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.utils import utils
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.resources_utils import get_resource


class FolderIcon(QWidget):
    def __init__(self, parent: QWidget, label_text: str):
        super().__init__(parent)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(rt(2))
        self.icon = QLabel(self)
        self.icon.setPixmap(QIcon(get_resource('resources/icons/folder.svg'))
                            .pixmap(QSize(rt(16), rt(16))))
        self.horizontal_layout.addWidget(self.icon)
        self.label = QLabel(self)
        self.label.setText(label_text)
        font = QtGui.QFont()
        font.setPointSize(applyFontRatio(11))
        self.label.setFont(font)
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
        self.main_layout.setContentsMargins(rt(3), 0, 0, 0)
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
        while self.calculateCurrentWidth() < self.max_width - rt(50) and i >= 0:
            self.labels[i].label.setMaximumWidth(999)
            i -= 1

        j = 0
        while self.calculateCurrentWidth() > self.max_width - rt(50) and j < len(self.labels):
            self.labels[j].label.setMaximumWidth(0)
            j += 1

    def resizeEvent(self, event: QResizeEvent):
        self.max_width = event.size().width()
        self.resizePaths()
        QWidget.resizeEvent(self, event)