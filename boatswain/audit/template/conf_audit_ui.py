from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame

from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy


class ConfAuditUi(QWidget):

    def __init__(self, parent, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)
        self.widget = QWidget(self)
        self.widget.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout.addWidget(self.widget)
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(rt(8), rt(2), rt(8), rt(5))
        self.type = QLabel(self.widget)
        self.horizontal_layout.addWidget(self.type)
        self.name = QLabel(self.widget)
        self.name.setSizePolicy(BQSizePolicy(h_stretch=2))
        self.horizontal_layout.addWidget(self.name)
        self.delete = QPushButton(self.widget)
        self.delete.setFlat(True)
        padding = "%dpx %dpx" % (1, rt(10))
        self.delete.setStyleSheet("border: 1px solid #999999; padding: %s; border-radius: 2px" % padding)
        self.horizontal_layout.addWidget(self.delete)
        self.delete.setText('Undo')
