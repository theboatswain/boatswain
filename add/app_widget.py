from PyQt5.QtCore import QMetaObject, QCoreApplication, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QPushButton, QWidget, QVBoxLayout


class AppWidget(object):

    def __init__(self, widget, name, description, pixmap) -> None:
        super().__init__()
        self.horizontalLayout = QHBoxLayout(widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.pic = QLabel(widget)
        self.pic.setMaximumSize(40, 40)
        self.pic.setPixmap(pixmap.scaled(40, 40, Qt.KeepAspectRatio))
        self.horizontalLayout.addWidget(self.pic)

        self.infoWidget = QWidget(widget)
        self.infoWidget.setObjectName("infoWidget")
        self.infoLayout = QVBoxLayout(self.infoWidget)
        self.infoLayout.setContentsMargins(5, 0, 0, 0)

        self.name = QLabel(widget)
        self.name.setObjectName("name")
        self.infoLayout.addWidget(self.name)

        self.description = QLabel(widget)
        self.description.setWordWrap(True)
        self.description.setObjectName("description")
        self.infoLayout.addWidget(self.description)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)

        self.infoWidget.setSizePolicy(sizePolicy)
        self.horizontalLayout.addWidget(self.infoWidget)
        self.fromRepo = QLabel(widget)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fromRepo.setFont(font)
        self.fromRepo.setObjectName("fromRepo")
        self.horizontalLayout.addWidget(self.fromRepo)
        self.install = QPushButton(widget)
        self.install.setObjectName("install")
        self.horizontalLayout.addWidget(self.install)

        _translate = QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "widget"))
        self.description.setText(_translate("widget", description))
        self.fromRepo.setText(_translate("widget", "From Dockerhub"))
        self.install.setText(_translate("widget", "Install"))
        self.name.setText(_translate("widget", name))
        QMetaObject.connectSlotsByName(widget)
