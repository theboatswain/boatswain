from PyQt5.QtCore import pyqtSlot, Qt, QMetaObject, QCoreApplication, QRect, QSize
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QLineEdit, QWidget, QSizePolicy, QVBoxLayout, QAction, \
    QStatusBar, QMenu, QMenuBar, QFrame, QScrollArea, QPushButton, QGridLayout, QComboBox

from controllers.add.add_app import AddAppDialog
from controllers.home.app_widget import AppWidget
from domains.container import Container
from services import data_transporter_service
from utils.constants import CONTAINER_CHANNEL, APP_EXIT_CHANNEL
from utils.custom_ui import BQSizePolicy


class Home(QMainWindow):

    def __init__(self):
        super(Home, self).__init__()
        self.setupUi(self)
        self.show()
        data_transporter_service.listen(CONTAINER_CHANNEL, self.addAppFromContainer)

        self.searchResultArea = QWidget(self)
        self.searchResultArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        layout = QVBoxLayout(self.searchResultArea)
        layout.setAlignment(Qt.AlignTop)
        self.searchResultArea.setLayout(layout)
        self.searchResultArea.layout().setContentsMargins(8, 12, 0, 12)
        self.scrollArea.setWidget(self.searchResultArea)
        self.scrollArea.setContentsMargins(0, 0, 0, 0)

    def setupUi(self, parentWidget):
        parentWidget.resize(460, 639)
        parentWidget.setSizePolicy(BQSizePolicy(h_stretch=1))
        parentWidget.setMinimumSize(QSize(460, 639))
        self.centralWidget = QWidget(parentWidget)
        self.centralWidget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.mainLayout = QVBoxLayout(self.centralWidget)
        self.mainLayout.setContentsMargins(11, 5, 11, 11)
        self.mainLayout.setSpacing(0)
        self.widget = QWidget(self.centralWidget)
        self.widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("border-bottom: 1px solid #999999")
        self.topLayout = QGridLayout(self.widget)
        self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setSpacing(6)
        self.appType = QComboBox(self.widget)
        self.appType.setSizePolicy(BQSizePolicy(h_stretch=1, width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.appType.setFocusPolicy(Qt.ClickFocus)
        self.appType.setObjectName("appType")
        self.appType.addItem("")
        self.appType.addItem("")
        self.appType.addItem("")
        self.topLayout.addWidget(self.appType, 0, 2, 1, 1)
        self.searchApp = QLineEdit(self.widget)
        self.searchApp.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.searchApp.setFocusPolicy(Qt.ClickFocus)
        self.searchApp.setStyleSheet("padding: 2 2 2 5;")
        self.searchApp.setObjectName("searchApp")
        self.topLayout.addWidget(self.searchApp, 0, 3, 1, 1)
        self.addApp = QPushButton(self.widget)
        self.addApp.setSizePolicy(BQSizePolicy(width=QSizePolicy.Minimum, height=QSizePolicy.Fixed))
        self.addApp.setFocusPolicy(Qt.ClickFocus)
        self.addApp.setObjectName("addApp")
        self.topLayout.addWidget(self.addApp, 0, 0, 1, 1)
        self.hiddenWidget = QWidget(self.widget)
        self.hiddenWidget.setSizePolicy(BQSizePolicy())
        self.topLayout.addWidget(self.hiddenWidget, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.widget)
        self.scrollArea = QScrollArea(self.centralWidget)
        self.scrollArea.setSizePolicy(BQSizePolicy(v_stretch=20))
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scrollArea)
        parentWidget.setCentralWidget(self.centralWidget)

        self.menuBar = QMenuBar(parentWidget)
        self.menuBar.setGeometry(QRect(0, 0, 460, 22))
        self.menuFile = QMenu(self.menuBar)
        parentWidget.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(parentWidget)
        parentWidget.setStatusBar(self.statusBar)
        self.actionAdd = QAction(parentWidget)
        self.actionAdd.setObjectName("actionAdd")
        self.menuFile.addAction(self.actionAdd)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslateUi(parentWidget)
        QMetaObject.connectSlotsByName(parentWidget)

    def retranslateUi(self, Boatswain):
        _translate = QCoreApplication.translate
        Boatswain.setWindowTitle(_translate("Boatswain", "Boatswain"))
        self.appType.setItemText(0, _translate("Boatswain", "All apps"))
        self.appType.setItemText(1, _translate("Boatswain", "Running"))
        self.appType.setItemText(2, _translate("Boatswain", "Stopped"))
        self.searchApp.setPlaceholderText(_translate("Boatswain", "Filter apps"))
        self.addApp.setText(_translate("Boatswain", "Add"))
        self.menuFile.setTitle(_translate("Boatswain", "File"))
        self.actionAdd.setText(_translate("Boatswain", "Add new app"))

    @pyqtSlot(bool, name='on_addApp_clicked')
    @pyqtSlot(bool, name='on_actionAdd_triggered')
    def addAppClicked(self, checked=None):
        if checked is None:
            return
        dialog = QDialog()
        dialog.ui = AddAppDialog("Add app", dialog)
        dialog.exec_()

    def addAppFromContainer(self, container: Container):
        widget = AppWidget(self.searchResultArea, container)
        self.searchResultArea.layout().addWidget(widget)

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)

    def closeEvent(self, event):
        data_transporter_service.fire(APP_EXIT_CHANNEL, True)
        event.accept()
