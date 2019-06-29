from PyQt5.QtCore import QMetaObject, QCoreApplication, pyqtSlot, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget, QVBoxLayout

from common.services import containers_service
from common.utils import text_utils
from common.utils.app_avatar import AppAvatar
from common.utils.custom_ui import BQSizePolicy


class AddAppWidget(QWidget):

    def __init__(self, parent, name, description) -> None:
        super().__init__(parent)
        self.horizontal_layout = QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        _translate = QCoreApplication.translate

        img_name = name
        name_part = name.split('/')
        if len(name_part) > 1:
            img_name = name_part[1]
        self.pic = AppAvatar(text_utils.getSimpleName(img_name), parent=self)
        self.horizontal_layout.addWidget(self.pic)

        self.info_widget = QWidget(self)
        self.info_layout = QVBoxLayout(self.info_widget)
        self.info_layout.setContentsMargins(5, 0, 0, 0)

        self.name = QLabel(self)
        self.name.setObjectName("name")
        self.info_layout.addWidget(self.name)

        if len(description) > 0:
            self.description = QLabel(self)
            self.description.setWordWrap(True)
            self.description.setObjectName("description")
            self.description.setText(_translate("widget", description))
            self.info_layout.addWidget(self.description)
        self.info_widget.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.horizontal_layout.addWidget(self.info_widget)
        self.from_repo = QLabel(self)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.from_repo.setFont(font)
        self.from_repo.setObjectName("fromRepo")
        self.horizontal_layout.addWidget(self.from_repo)
        self.install = QPushButton(self)
        self.install.setObjectName("install")
        self.install.setFocusPolicy(Qt.NoFocus)
        self.horizontal_layout.addWidget(self.install)
        self.from_repo.setText(_translate("widget", "From Dockerhub"))
        self.install.setText(_translate("widget", "Install"))
        self.name.setText(_translate("widget", name))
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot(bool, name='on_install_clicked')
    def installApp(self, checked):
        containers_service.installContainer(self.name.text(), self.description.text())
