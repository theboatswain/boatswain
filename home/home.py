from PyQt5.QtCore import pyqtSlot, Qt, QMetaObject, QCoreApplication, QRect, QSize
from PyQt5.QtWidgets import QMainWindow, QDialog, QApplication, QLineEdit, QWidget, QSizePolicy, QVBoxLayout, QAction, \
    QStatusBar, QMenu, QMenuBar, QFrame, QScrollArea, QPushButton, QGridLayout, QComboBox

from app.add_app import AddAppDialog
from common.models.container import Container
from common.services import data_transporter_service
from common.utils.constants import CONTAINER_CHANNEL, APP_EXIT_CHANNEL, ADD_APP_CHANNEL
from common.utils.custom_ui import BQSizePolicy
from home.app_widget import AppWidget


class Home(QMainWindow):
    """ Home screen """

    def __init__(self):
        super(Home, self).__init__()
        self.setupUi(self)
        self.show()
        data_transporter_service.listen(CONTAINER_CHANNEL, self.addAppFromContainer)
        data_transporter_service.listen(ADD_APP_CHANNEL, self.addAppClicked)
        self.app_list = QWidget(self)
        self.app_list.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        layout = QVBoxLayout(self.app_list)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        layout.setContentsMargins(0, 1, 0, 0)
        self.app_list.setLayout(layout)
        self.scroll_area.setWidget(self.app_list)

    def setupUi(self, parent_widget):
        parent_widget.resize(460, 639)
        parent_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        parent_widget.setMinimumSize(QSize(460, 639))
        central_widget = QWidget(parent_widget)
        central_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 5, 0, 11)
        main_layout.setSpacing(0)
        widget = QWidget(central_widget)
        widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        widget.setAutoFillBackground(False)
        top_layout = QGridLayout(widget)
        top_layout.setContentsMargins(11, 0, 11, 11)
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
        self.add_app = QPushButton(widget)
        self.add_app.setSizePolicy(BQSizePolicy(width=QSizePolicy.Minimum, height=QSizePolicy.Fixed))
        self.add_app.setFocusPolicy(Qt.ClickFocus)
        self.add_app.setObjectName("addApp")
        top_layout.addWidget(self.add_app, 0, 0, 1, 1)

        hidden_widget = QWidget(widget)
        hidden_widget.setSizePolicy(BQSizePolicy())
        top_layout.addWidget(hidden_widget, 0, 1, 1, 1)

        main_layout.addWidget(widget)

        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        self.scroll_area = QScrollArea(central_widget)
        self.scroll_area.setSizePolicy(BQSizePolicy(v_stretch=20))
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)
        parent_widget.setCentralWidget(central_widget)

        self.menu_bar = QMenuBar(parent_widget)
        self.menu_bar.setGeometry(QRect(0, 0, 460, 22))
        self.menu_file = QMenu(self.menu_bar)
        parent_widget.setMenuBar(self.menu_bar)
        self.status_bar = QStatusBar(parent_widget)
        parent_widget.setStatusBar(self.status_bar)
        self.action_add = QAction(parent_widget)
        self.action_add.setObjectName("actionAdd")
        self.menu_file.addAction(self.action_add)
        self.menu_bar.addAction(self.menu_file.menuAction())

        self.retranslateUi(parent_widget)
        QMetaObject.connectSlotsByName(parent_widget)

    def retranslateUi(self, boatswain):
        _translate = QCoreApplication.translate
        boatswain.setWindowTitle(_translate("Boatswain", "Boatswain"))
        self.app_type.setItemText(0, _translate("Boatswain", "All apps"))
        self.app_type.setItemText(1, _translate("Boatswain", "Running"))
        self.app_type.setItemText(2, _translate("Boatswain", "Stopped"))
        self.search_app.setPlaceholderText(_translate("Boatswain", "Filter apps"))
        self.add_app.setText(_translate("Boatswain", "Add"))
        self.menu_file.setTitle(_translate("Boatswain", "File"))
        self.action_add.setText(_translate("Boatswain", "Add new app"))

    @pyqtSlot(bool, name='on_addApp_clicked')
    @pyqtSlot(bool, name='on_actionAdd_triggered')
    def addAppClicked(self, checked=None):
        if checked is None:
            return
        dialog = QDialog()
        dialog.ui = AddAppDialog("Add app", dialog)
        dialog.exec_()

    def addAppFromContainer(self, container: Container):
        widget = AppWidget(self.app_list, container)
        self.app_list.layout().addWidget(widget)

    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, QLineEdit):
            focused_widget.clearFocus()
        QMainWindow.mousePressEvent(self, event)

    def closeEvent(self, event):
        data_transporter_service.fire(APP_EXIT_CHANNEL, True)
        QMainWindow.closeEvent(self, event)
