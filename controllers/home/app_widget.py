from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QPushButton, QWidget, QVBoxLayout

from domains.container import Container
from services import containers_service
from utils import text_utils
from utils.app_avatar import AppAvatar


class AppWidget(QWidget):

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.setMinimumHeight(50)
        self.setMaximumHeight(50)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        _translate = QCoreApplication.translate

        img_name = container.name
        name_part = container.name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=self, radius=22)
        self.horizontalLayout.addWidget(self.pic)

        self.infoWidget = QWidget(self)
        self.infoWidget.setObjectName("infoWidget")
        self.infoLayout = QVBoxLayout(self.infoWidget)
        self.infoLayout.setContentsMargins(5, 0, 0, 0)

        self.name = QLabel(self)
        self.name.setObjectName("name")
        self.infoLayout.addWidget(self.name)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)

        self.infoWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.infoWidget)

        self.start = QPushButton(self)
        self.start.setObjectName("start")
        self.horizontalLayout.addWidget(self.start)
        self.start.setText(_translate("widget", "Start"))
        self.name.setText(_translate("widget", container.name))

        QMetaObject.connectSlotsByName(self)

