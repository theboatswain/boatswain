from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QLabel, QPushButton

from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.common.utils.app_avatar import AppAvatar


class AppearanceUnitUi(QWidget):

    selected = pyqtSignal()

    def __init__(self, parent, theme_name, definition: str, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(rt(20), rt(11), rt(20), rt(11))
        self.vertical_layout.setSpacing(rt(6))
        self.vertical_layout.setAlignment(Qt.AlignCenter)
        self.visualise = QWidget(self)
        self.visualise.setSizePolicy(BQSizePolicy(v_stretch=3))
        self.visualise.setFixedSize(QSize(rt(80), rt(50)))
        self.visualise.setProperty('class', 'home')
        self.visualise.setStyleSheet("QWidget.home { border-radius: 8px; }")
        self.setProperty('class', 'Theme' + theme_name)

        self.app_widget_layout = QVBoxLayout(self.visualise)
        self.app_widget_layout.setContentsMargins(0, 12, 0, 10)
        self.app_widget_layout.setSpacing(0)

        line = QFrame(self.visualise)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        self.app_widget_layout.addWidget(line)

        widget = QWidget(self.visualise)
        widget.setProperty('class', 'app-widget')
        self.app_widget_layout.addWidget(widget)
        self.app_horizontal_layout = QHBoxLayout(widget)
        self.app_horizontal_layout.setContentsMargins(rt(4), 0, rt(4), 0)
        self.app_horizontal_layout.setSpacing(2)
        pic = AppAvatar(None, "Sample", parent=widget, radius=rt(5), font_size=applyFontRatio(7))
        self.app_horizontal_layout.addWidget(pic)

        font = QFont()
        font.setPointSize(applyFontRatio(2))

        name = QLabel(widget)
        name.setFont(font)
        name.setText("Sample application")
        name.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.app_horizontal_layout.addWidget(name)

        status = QPushButton(widget)
        status.setFlat(True)
        status.setFont(font)
        status.setProperty('class', 'bordered-widget')
        status.setStyleSheet('padding: 0 %dpx' % rt(1))
        self.app_horizontal_layout.addWidget(status)

        line = QFrame(self.visualise)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        self.app_widget_layout.addWidget(line)

        self.vertical_layout.addWidget(self.visualise)

        label = QtWidgets.QLabel(self)
        label.setText(theme_name)
        label.setAlignment(Qt.AlignCenter)
        self.vertical_layout.addWidget(label)
        self.setStyleSheet(definition)

    def mouseReleaseEvent(self, event) -> None:
        self.selected.emit()
