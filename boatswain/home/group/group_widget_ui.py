from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QLineEdit, QLabel, QLayout

from boatswain.common.models.group import Group
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.resources_utils import get_resource


class GroupWidgetUi(QWidget):
    """ Class to customise group's widgets """

    def __init__(self, parent, group: Group, handler) -> None:
        super().__init__(parent)
        self.handler = handler
        self.group = group
        self.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setAlignment(Qt.AlignTop)
        self.main_layout.setSpacing(0)

        self.top_widget = QWidget(self)
        self.top_widget.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        top_layout = QHBoxLayout(self.top_widget)
        top_layout.setContentsMargins(rt(11), rt(5), 0, rt(5))
        top_layout.setSpacing(rt(6))

        # self.direction = QLabel(self)
        # self.direction.setText("⌄")
        # top_layout.addWidget(self.direction)

        self.icon = QLabel(self)
        self.icon.setPixmap(QIcon(get_resource('resources/icons/folder.svg'))
                            .pixmap(QSize(rt(16), rt(16))))
        top_layout.addWidget(self.icon)
        self.container_name = QLineEdit(self.top_widget)

        # Remove the border outline on focus
        self.container_name.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.container_name.setStyleSheet('border: none; background-color: transparent')
        self.container_name.setReadOnly(True)
        self.container_name.setText(self.group.name)
        top_layout.addWidget(self.container_name)

        self.main_layout.addWidget(self.top_widget)
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.main_layout.addWidget(self.line)

        self.app_list = QWidget(self)
        self.app_list.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.app_list_layout = QVBoxLayout(self.app_list)
        self.app_list_layout.setSpacing(0)
        self.app_list_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.app_list_layout.setAlignment(Qt.AlignTop)
        self.app_list_layout.setContentsMargins(0, rt(1), 0, 0)
        self.app_list.setLayout(self.app_list_layout)

        self.main_layout.addWidget(self.app_list)
