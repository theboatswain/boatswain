from PyQt5.QtWidgets import QWidget, QSizePolicy, QGridLayout, QPushButton

from common.models.container import Container
from common.utils.custom_ui import BQSizePolicy


class AdvancedAppWidget(QWidget):

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.layout = QGridLayout(self)
        self.layout.addWidget(QPushButton(self))
