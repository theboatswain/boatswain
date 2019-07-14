from PyQt5.QtCore import QCoreApplication, Qt, QSize, QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QDialog

from common.models.container import Container
from common.utils.custom_ui import BQSizePolicy, AutoResizeWidget
from config.configures.environment import EnvironmentVariable
from config.configures.general import GeneralAppConfig


class AppConfig(object):

    def __init__(self, title, dialog: QDialog, container: Container) -> None:
        super().__init__()
        self.title = title
        self.container = container
        self.setupUi(dialog)
        self.dialog = dialog
        dialog.setWindowTitle(self.title)
        dialog.setAttribute(Qt.WA_DeleteOnClose)

    def setupUi(self, dialog):
        dialog.resize(745, 445)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumSize(QSize(745, 445))
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)

        main_layout = QVBoxLayout(dialog)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.central_widget = QWidget(dialog)
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.vertical_layout.setContentsMargins(11, 11, 11, 15)
        self.vertical_layout.setSpacing(6)
        self.tab_widget = QTabWidget(self.central_widget)
        self.tab_widget.setObjectName("tabs")
        self.tab_widget.setDocumentMode(False)
        self.general = GeneralAppConfig(self.central_widget, self.container)
        self.tab_widget.addTab(self.general, "")
        self.port = AutoResizeWidget(self.central_widget)
        self.tab_widget.addTab(self.port, "")
        self.volume = AutoResizeWidget(self.central_widget)
        self.tab_widget.addTab(self.volume, "")
        self.environment = EnvironmentVariable(self.central_widget, self.container)
        self.tab_widget.addTab(self.environment, "")
        self.others = AutoResizeWidget(self.central_widget)
        self.tab_widget.addTab(self.others, "")
        self.vertical_layout.addWidget(self.tab_widget)

        main_layout.addWidget(self.central_widget)

        self.retranslateUi()
        self.tab_widget.setCurrentIndex(0)
        self.tab_widget.currentChanged.connect(self.onTabChange)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.general), _translate("MainWindow", "General"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.port), _translate("MainWindow", "Port mapping"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.volume), _translate("MainWindow", "Volume mount"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.environment), _translate("MainWindow", "Environment"))
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.others), _translate("MainWindow", "Others"))

    def onTabChange(self, index):
        widget = self.tab_widget.widget(index)
        self.dialog.resize(widget.preferableSize())
        # prevWidget = self.tab_widget.currentWidget()
        # self.animation = QPropertyAnimation(self.dialog, b"maximumSize")
        # self.animation.setDuration(300)
        # self.animation.setStartValue(prevWidget.preferableSize())
        # self.animation.setEndValue(widget.preferableSize())
        # self.animation.start()
