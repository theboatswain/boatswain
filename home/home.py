from PyQt5.QtCore import pyqtSlot, Qt, QMetaObject, QCoreApplication, QRect, QSize
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QLineEdit, QWidget, QSizePolicy, QVBoxLayout, QAction, \
    QStatusBar, QMenu, QMenuBar, QFrame, QScrollArea, QPushButton, QGridLayout, QComboBox

from app.add_app import AddAppDialog
from home.app_widget import AppWidget
from common.models.container import Container
from home import data_transporter_service
from common.utils.constants import CONTAINER_CHANNEL, APP_EXIT_CHANNEL
from common.utils.custom_ui import BQSizePolicy


class Home(QMainWindow):
    """ Home screen """

    def __init__(self):
        super(Home, self).__init__()
        self.setup_ui(self)
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

    def setup_ui(self, parent_widget):
        parent_widget.resize(460, 639)
        parent_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        parent_widget.setMinimumSize(QSize(460, 639))
        central_widget = QWidget(parent_widget)
        central_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(11, 5, 11, 11)
        main_layout.setSpacing(0)
        widget = QWidget(central_widget)
        widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        widget.setAutoFillBackground(False)
        widget.setStyleSheet("border-bottom: 1px solid #999999")
        top_layout = QGridLayout(widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(6)
        self.app_type = QComboBox(widget)
        self.app_type.setSizePolicy(BQSizePolicy(h_stretch=1, width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.app_type.setFocusPolicy(Qt.ClickFocus)
        self.app_type.setObjectName("appType")
        self.app_type.addItem("")
        self.app_type.addItem("")
        self.app_type.addItem("")
        top_layout.addWidget(self.app_type, 0, 2, 1, 1)
        self.search_app = QLineEdit(widget)
        self.search_app.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.search_app.setFocusPolicy(Qt.ClickFocus)
        self.search_app.setStyleSheet("padding: 2 2 2 5;")
        self.search_app.setObjectName("searchApp")
        top_layout.addWidget(self.search_app, 0, 3, 1, 1)
        self.addApp = QPushButton(widget)
        self.addApp.setSizePolicy(BQSizePolicy(width=QSizePolicy.Minimum, height=QSizePolicy.Fixed))
        self.addApp.setFocusPolicy(Qt.ClickFocus)
        self.addApp.setObjectName("addApp")
        top_layout.addWidget(self.addApp, 0, 0, 1, 1)
        hidden_widget = QWidget(widget)
        hidden_widget.setSizePolicy(BQSizePolicy())
        top_layout.addWidget(hidden_widget, 0, 1, 1, 1)
        main_layout.addWidget(widget)
        self.scrollArea = QScrollArea(central_widget)
        self.scrollArea.setSizePolicy(BQSizePolicy(v_stretch=20))
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        main_layout.addWidget(self.scrollArea)
        parent_widget.setCentralWidget(central_widget)

        self.menuBar = QMenuBar(parent_widget)
        self.menuBar.setGeometry(QRect(0, 0, 460, 22))
        self.menuFile = QMenu(self.menuBar)
        parent_widget.setMenuBar(self.menuBar)
        self.statusBar = QStatusBar(parent_widget)
        parent_widget.setStatusBar(self.statusBar)
        self.actionAdd = QAction(parent_widget)
        self.actionAdd.setObjectName("actionAdd")
        self.menuFile.addAction(self.actionAdd)
        self.menuBar.addAction(self.menuFile.menuAction())

        self.retranslate_ui(parent_widget)
        QMetaObject.connectSlotsByName(parent_widget)

    def retranslate_ui(self, boatswain):
        _translate = QCoreApplication.translate
        boatswain.setWindowTitle(_translate("Boatswain", "Boatswain"))
        self.app_type.setItemText(0, _translate("Boatswain", "All apps"))
        self.app_type.setItemText(1, _translate("Boatswain", "Running"))
        self.app_type.setItemText(2, _translate("Boatswain", "Stopped"))
        self.search_app.setPlaceholderText(_translate("Boatswain", "Filter apps"))
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
