from PyQt5.QtCore import QObject, QPropertyAnimation, Qt
from PyQt5.QtGui import QMouseEvent

from boatswain.common.models.group import Group
from boatswain.home.group.group_widget_ui import GroupWidgetUi


class GroupWidget(QObject):
    max_height: int

    def __init__(self, group: Group, parent=None):
        super().__init__(parent)
        self.group = group
        self.ui = GroupWidgetUi(parent, group, self)
        self.is_mouse_released = True
        self.ui.container_name.mouseReleaseEvent = self.onMouseReleased
        self.ui.top_widget.mouseReleaseEvent = self.onMouseReleased

    def onMouseReleased(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_mouse_released = True
            self.toggleWindow()

    def toggleWindow(self):
        if self.ui.app_list.maximumHeight() == 0:
            self.animation = QPropertyAnimation(self.ui.app_list, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.max_height)
            self.animation.start()
        else:
            self.max_height = 0
            for i in range(self.ui.app_list_layout.count()):
                self.max_height += self.ui.app_list_layout.itemAt(i).widget().max_height
            self.animation = QPropertyAnimation(self.ui.app_list, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setStartValue(self.max_height)
            self.animation.setEndValue(0)
            self.animation.start()
