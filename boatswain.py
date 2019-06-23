import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow


class Boatswain(QMainWindow):
    def __init__(self):
        super(Boatswain, self).__init__()
        uic.loadUi('boatswain.ui', self)

        self.show()
        self.addApp.clicked.connect(self.addInputTextToListbox)

    def addInputTextToListbox(self):
        print("asdasd")

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Boatswain()
    sys.exit(app.exec_())
