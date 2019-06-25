from PyQt5.QtCore import QMetaObject, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QPushButton


class AppWidget(object):

    def __init__(self, widget, name, description) -> None:
        super().__init__()
        self.horizontalLayout = QHBoxLayout(widget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.name = QLabel(widget)
        self.name.setObjectName("name")
        self.horizontalLayout.addWidget(self.name)

        self.description = QLabel(widget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.description.sizePolicy().hasHeightForWidth())
        self.description.setSizePolicy(sizePolicy)
        self.description.setWordWrap(True)
        self.description.setObjectName("description")
        self.horizontalLayout.addWidget(self.description)
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
