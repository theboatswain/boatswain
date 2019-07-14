from PyQt5.QtCore import QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QWidget, QStyle, QToolButton, QLineEdit, QFileDialog, QItemDelegate


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


class PathInputDelegate(QItemDelegate):

    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):

        editor = ButtonLineEdit('config/icons/directory.png', parent=parent)
        editor.setText(str(index.data()))
        editor.buttonClicked.connect(lambda x: self.fileLooking(editor))
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setText(str(index.data()))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text())

    @pyqtSlot()
    def currentIndexChanged(self):
        self.commitData.emit(self.sender())

    def fileLooking(self, editor):
        file = str(QFileDialog.getExistingDirectory(self.parent(), "Select Directory"))
        if file:
            editor.setText(file)


class ButtonLineEdit(QLineEdit):
    buttonClicked = pyqtSignal(bool)

    def __init__(self, icon_file, parent=None):
        super(ButtonLineEdit, self).__init__(parent)

        self.button = QToolButton(self)
        self.button.setIcon(QIcon(icon_file))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(Qt.OpenHandCursor)
        self.button.clicked.connect(self.buttonClicked.emit)

        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()

        self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth * 2 + 2),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth * 2 + 2))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),
                         (self.rect().bottom() - buttonSize.height() + 1)/2)
        super(ButtonLineEdit, self).resizeEvent(event)