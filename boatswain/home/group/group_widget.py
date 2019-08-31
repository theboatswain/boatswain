from PyQt5.QtCore import QObject, QPropertyAnimation, Qt, QMimeData, QPoint, QTimer, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QDrag, QPixmap, QRegion, QDragEnterEvent, QDragMoveEvent, QPalette, QColor, \
    QDragLeaveEvent, QDropEvent, QFocusEvent, QKeyEvent
from PyQt5.QtWidgets import QLayout, QApplication, QWidget, QMenu, QLineEdit, QMessageBox
from boatswain.common.utils.constants import ADD_APP_CHANNEL

from boatswain.common.models.container import Container
from boatswain.common.models.group import Group
from boatswain.common.services import containers_service, group_service, data_transporter_service
from boatswain.home.group.group_widget_ui import GroupWidgetUi


class GroupWidget(QObject):
    animation: QPropertyAnimation
    move_app = pyqtSignal(Container, GroupWidgetUi)
    move_group = pyqtSignal(Group, GroupWidgetUi)

    def __init__(self, group: Group, parent=None):
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
        delete.triggered.connect(self.onDeleteGroupTriggered)
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

    def onDeleteGroupTriggered(self):
        if self.group.is_default:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText(self.tr("Unable to delete group"))
            msg.setInformativeText(self.tr("You can't delete default group!!!"))
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
            return
        message = self.tr("Are you sure you want to delete this folder? All apps inside will be deleted also!")
        button_reply = QMessageBox.question(self.ui, 'Delete folder', message,
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if button_reply == QMessageBox.Ok:
            for i in reversed(range(self.ui.app_list_layout.count())):
                container = self.ui.app_list_layout.itemAt(i).widget().container
                containers_service.deleteContainer(container)
                self.ui.app_list_layout.itemAt(i).widget().setParent(None)
            group_service.deleteGroup(self.group)
            self.ui.deleteLater()