from PyQt5.QtCore import QMetaObject, QCoreApplication, pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QPushButton, QWidget, QVBoxLayout

from app import containers_service
from common.utils import text_utils
from common.utils.app_avatar import AppAvatar


class AddAppWidget(QWidget):

    def __init__(self, parent, name, description) -> None:
        super().__init__(parent)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        _translate = QCoreApplication.translate

        img_name = name
        name_part = name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=self)
        self.horizontalLayout.addWidget(self.pic)

        self.infoWidget = QWidget(self)
        self.infoWidget.setObjectName("infoWidget")
        self.infoLayout = QVBoxLayout(self.infoWidget)
        self.infoLayout.setContentsMargins(5, 0, 0, 0)

        self.name = QLabel(self)
        self.name.setObjectName("name")
        self.infoLayout.addWidget(self.name)

        if len(description) > 0:
            self.description = QLabel(self)
            self.description.setWordWrap(True)
            self.description.setObjectName("description")
            self.description.setText(_translate("widget", description))
            self.infoLayout.addWidget(self.description)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)

        self.infoWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.infoWidget)
        self.fromRepo = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fromRepo.setFont(font)
        self.fromRepo.setObjectName("fromRepo")
        self.horizontalLayout.addWidget(self.fromRepo)
        self.install = QPushButton(self)
        self.install.setObjectName("install")
        self.horizontalLayout.addWidget(self.install)
        self.fromRepo.setText(_translate("widget", "From Dockerhub"))
        self.install.setText(_translate("widget", "Install"))
        self.name.setText(_translate("widget", name))
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot(bool, name='on_install_clicked')
    def installApp(self, checked):
        containers_service.install_container(self.name.text(), self.description.text())
