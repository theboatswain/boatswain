from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout, QSizePolicy, QFrame

from common.models.container import Container
from common.utils import text_utils
from common.utils.app_avatar import AppAvatar
from common.utils.custom_ui import BQSizePolicy


class AppWidget(QWidget):
    """ Class to customise app's widgets """
    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 2, 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setAlignment(Qt.AlignTop)
        widget = QWidget(self)
        widget.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout.addWidget(widget)
        self.horizontal_layout = QHBoxLayout(widget)
        self.horizontal_layout.setContentsMargins(20, 2, 10, 5)
        _translate = QCoreApplication.translate

        img_name = container.name
        name_part = container.name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=widget, radius=21)
        self.horizontal_layout.addWidget(self.pic)
        self.name = QLabel(widget)
        self.name.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.name.setObjectName("name")
        self.horizontal_layout.addWidget(self.name)

        self.start = QPushButton(widget)
        self.start.setObjectName("start")
        self.start.setFlat(True)
        self.start.setStyleSheet("border: 1px solid #999999; padding: 1px 10px; border-radius: 2px")
        self.horizontal_layout.addWidget(self.start)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.vertical_layout.addWidget(line)

        self.start.setText(_translate("widget", "Start"))
        self.name.setText(_translate("widget", container.name))

        QMetaObject.connectSlotsByName(self)
