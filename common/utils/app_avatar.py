from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class AppAvatar(QWidget):
    """ Class to customise app's avatar """

    def __init__(self, name, radius=25, parent=None):
        super().__init__(parent)
        self.setFixedSize(radius * 2, radius * 2)
        self.avatarLayout = QVBoxLayout(self)
        self.avatarLayout.setContentsMargins(0, 0, 0, 0)
        self.name = QLabel(self)
        self.name.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(20)
        self.name.setFont(font)
        self.avatarLayout.addWidget(self.name, Qt.AlignCenter)
        _translate = QCoreApplication.translate
        self.name.setText(_translate("widget", name))
        self.w_width = radius * 2
        self.w_height = radius * 2
        self.setLayout(self.avatarLayout)
        self.setStyleSheet("border-radius: " + str(radius) + "px; background: rgb(89, 173, 223); color: white")
