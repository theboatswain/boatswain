from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

from common.models.container import Container
from common.utils.custom_ui import BQSizePolicy


class AppInfoWidget(QWidget):
    """Class to customise the basic app info, when user click into the AppWidget"""

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setAlignment(Qt.AlignTop)
        widget = QWidget(self)
        widget.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.vertical_layout.addWidget(widget)