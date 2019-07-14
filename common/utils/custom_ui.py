from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QSizePolicy, QWidget


class BQSizePolicy(QSizePolicy):
    def __init__(self, width=QSizePolicy.Preferred, height=QSizePolicy.Preferred, h_stretch=0, v_stretch=0):
        super().__init__(width, height)
        self.setHorizontalStretch(h_stretch)
        self.setVerticalStretch(v_stretch)


class ReloadableWidget(QWidget):
    def reloadData(self):
        raise NotImplementedError()


class AutoResizeWidget(QWidget):
    def preferableSize(self) -> QSize:
        return QSize(745, 445)
