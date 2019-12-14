#  This file is part of Boatswain.
#
#      Boatswain is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Boatswain is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5.QtCore import QObject, QPropertyAnimation, Qt, QMimeData, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QDrag, QPixmap, QRegion, QDragEnterEvent, QDragMoveEvent, QPalette, QColor, \
    QDragLeaveEvent, QDropEvent, QFocusEvent, QKeyEvent
from PyQt5.QtWidgets import QLayout, QApplication, QWidget, QMenu, QLineEdit

from boatswain.common.models.container import Container
from boatswain.common.models.group import Group
from boatswain.common.services import containers_service, group_service, data_transporter_service
from boatswain.common.utils.constants import ADD_APP_CHANNEL
from boatswain.home.group.group_widget_ui import GroupWidgetUi


class GroupWidget(QObject):
    animation: QPropertyAnimation
    move_app = pyqtSignal(Container, GroupWidgetUi)
    move_group = pyqtSignal(Group, GroupWidgetUi)
    delete_group = pyqtSignal(Group)

    def __init__(self, group: Group, parent=None, delete_action=None):
        super().__init__(parent)
        self.group = group
        self.ui = GroupWidgetUi(parent, group, self)
        self.is_mouse_released = True
        self.ui.container_name.mouseReleaseEvent = self.onMouseReleased
        self.ui.top_widget.mouseReleaseEvent = self.onMouseReleased
        self.ui.top_widget.mousePressEvent = self.mousePressEvent
        self.ui.container_name.mousePressEvent = self.mousePressEvent
        self.ui.container_name.dragEnterEvent = self.dragEnterEvent
        self.ui.container_name.dragLeaveEvent = self.dragLeaveEvent
        self.ui.container_name.dragMoveEvent = self.dragMoveEvent
        self.ui.container_name.dropEvent = self.dropEvent
        self.ui.container_name.contextMenuEvent = self.contextMenuEvent
        self.ui.container_name.returnPressed.connect(self.onRenamePerform)
        self.ui.container_name.focusOutEvent = self.onFocusOutEvent
        self.ui.container_name.keyPressEvent = self.nameEscEvent
        self.ui.top_widget.contextMenuEvent = self.contextMenuEvent
        if not self.group.expanded:
            self.ui.app_list_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
            self.ui.app_list.setMaximumHeight(0)
        self.ui.setAcceptDrops(True)
        self.cleanDraggingEffects()
        self.delete_action = delete_action

    def onMouseReleased(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_mouse_released = True
            self.toggleWindow()

    def onGroupExpanded(self):
        self.ui.app_list_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.ui.app_list.setMaximumHeight(99999)
        self.group.expanded = True
        self.group.save()

    def onGroupCollapsed(self):
        self.group.expanded = False
        self.group.save()

    def toggleWindow(self):
        self.animation = QPropertyAnimation(self.ui.app_list, b"maximumHeight")
        self.animation.setDuration(250)
        try:
            self.animation.finished.disconnect()
        except TypeError:
            pass
        if self.ui.app_list.maximumHeight() == 0:
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.ui.app_list_layout.sizeHint().height())
            self.animation.finished.connect(self.onGroupExpanded)
        else:
            self.ui.app_list_layout.setSizeConstraint(QLayout.SetDefaultConstraint)
            self.animation.setStartValue(self.ui.app_list_layout.sizeHint().height())
            self.animation.setEndValue(0)
            self.animation.finished.connect(self.onGroupCollapsed)
        self.animation.start()

    def cleanDraggingEffects(self):
        self.ui.line.setPalette(QApplication.palette(self.ui.line))
        self.ui.top_widget.setStyleSheet("""
                            .QWidget {
                                border: 1px solid transparent;
                            }
                            """)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.is_mouse_released = False
            timer = QTimer(self.ui)
            timer.setSingleShot(True)
            pos = event.pos()
            timer.timeout.connect(lambda: self.startDragging(pos))
            timer.start(200)

    def startDragging(self, pos):
        if not self.is_mouse_released:
            drag = QDrag(self.ui.top_widget)
            mime_data = QMimeData()
            mime_data.setText(str('Group:%d' % self.group.id))
            widget_pixmap = QPixmap(self.ui.top_widget.size())
            widget_pixmap.fill(Qt.transparent)
            self.ui.top_widget.render(widget_pixmap, QPoint(), QRegion(), QWidget.DrawChildren)
            drag.setMimeData(mime_data)
            drag.setPixmap(widget_pixmap)
            drag.setHotSpot(pos)
            drag.exec_()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            data: str = event.mimeData().text()
            if data.isdigit():
                event.acceptProposedAction()
            if 'Group:' in data:
                group_id = int(data.split('Group:')[1])
                if group_id != self.group.id:
                    event.acceptProposedAction()

    def dragMoveEvent(self, event: QDragMoveEvent):
        self.cleanDraggingEffects()
        if 'Group:' in event.mimeData().text():
            palette = self.ui.line.palette()
            palette.setColor(QPalette.Dark, QColor(89, 173, 223))
            self.ui.line.setPalette(palette)
        else:
            self.ui.top_widget.setStyleSheet("""
                    .QWidget {
                        border: 1px solid qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 blue,"""
                                             """ stop:0.5 rgb(89, 173, 223), stop:1 red);
                    }
                    """)

    def dragLeaveEvent(self, event: QDragLeaveEvent):
        self.cleanDraggingEffects()

    def dropEvent(self, event: QDropEvent):
        data: str = event.mimeData().text()
        if data.isdigit():
            container_id = int(event.mimeData().text())
            drop_container = containers_service.getContainer(container_id)
            drop_container.group = self.group
            drop_container.save()
            self.move_app.emit(drop_container, self.ui)
        else:
            group_id = int(data.split('Group:')[1])
            drop_group = group_service.getGroup(group_id)
            drop_group.order = group_service.getNextOrder(self.group)
            drop_group.save()
            self.move_group.emit(drop_group, self.ui)
        event.acceptProposedAction()
        self.cleanDraggingEffects()

    def contextMenuEvent(self, event):
        menu = QMenu(self.ui)
        add = menu.addAction(self.tr('Add app into this folder...'))
        add.triggered.connect(lambda: data_transporter_service.fire(ADD_APP_CHANNEL, self.group))
        menu.addSeparator()
        rename = menu.addAction(self.tr('Rename'))
        rename.triggered.connect(self.onRenameTriggered)
        delete = menu.addAction(self.tr('Delete'))
        delete.triggered.connect(lambda: self.delete_group.emit(self.group))
        menu.exec_(self.ui.mapToGlobal(event.pos()))

    def onRenameTriggered(self):
        self.ui.container_name.setReadOnly(False)
        self.ui.container_name.selectAll()

    def onRenamePerform(self):
        self.ui.container_name.setReadOnly(True)
        self.group.name = self.ui.container_name.text()
        self.group.save()

    def onFocusOutEvent(self, event: QFocusEvent):
        self.onRenamePerform()
        QLineEdit.focusOutEvent(self.ui.container_name, event)

    def nameEscEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.ui.container_name.setText(self.group.name)
            self.ui.container_name.setReadOnly(True)
        QLineEdit.keyPressEvent(self.ui.container_name, event)
