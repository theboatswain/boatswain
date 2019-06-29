from PyQt5.QtCore import QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from common.models.container import Container
from common.utils import text_utils
from common.utils.app_avatar import AppAvatar
from common.utils.custom_ui import BQSizePolicy


class AppWidget(QWidget):
    """ Class to customise app's widgets """
    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        _translate = QCoreApplication.translate

        img_name = container.name
        name_part = container.name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=self, radius=22)
        self.horizontal_layout.addWidget(self.pic)

        self.name = QLabel(self)
        self.name.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.name.setObjectName("name")
        self.horizontal_layout.addWidget(self.name)

        self.start = QPushButton(self)
        self.start.setObjectName("start")
        self.horizontal_layout.addWidget(self.start)
        self.start.setText(_translate("widget", "Start"))
        self.name.setText(_translate("widget", container.name))

        QMetaObject.connectSlotsByName(self)
