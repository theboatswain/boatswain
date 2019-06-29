import json

from PyQt5.QtCore import Qt, QCoreApplication, QMetaObject, QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QFrame, QScrollArea, QLineEdit, QComboBox, QGridLayout

from app.add_app_widget import AddAppWidget
from app.search.dockerhub_searcher import DockerHubSearcher
from app.search.search_images import DefaultSearchImages
from common.utils.custom_ui import BQSizePolicy


class AddAppDialog(object):

    def __init__(self, title, dialog) -> None:
        super().__init__()
        self.title = title
        self.setup_ui(dialog)
        dialog.setWindowTitle(self.title)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.searchResultArea = QWidget(dialog)
        self.searchResultArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.searchResultArea.setLayout(QVBoxLayout(self.searchResultArea))
        self.searchResultArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.searchResultArea)
        self.keySearch.returnPressed.connect(self.search_app)

        # Initialising search engines
        self.searchEngine = DefaultSearchImages()
        self.searchEngine = DockerHubSearcher(self.searchEngine)

        # Loading default search images
        with open('app/resources/default_search.json', 'r') as f:
            self.load_result(json.load(f))

    def setup_ui(self, add_app_dialog):
        add_app_dialog.resize(792, 387)
        add_app_dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        add_app_dialog.setMinimumSize(QSize(792, 387))
        add_app_dialog.setSizeGripEnabled(False)
        add_app_dialog.setModal(False)
        main_layout = QVBoxLayout(add_app_dialog)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(0)
        widget = QWidget(add_app_dialog)
        widget.setSizePolicy(BQSizePolicy())
        self.gridContainer = QGridLayout(widget)
        self.gridContainer.setContentsMargins(0, 0, 0, 0)
        self.comboBox = QComboBox(widget)
        self.comboBox.setSizePolicy(BQSizePolicy(width=QSizePolicy.Fixed, height=QSizePolicy.Fixed))
        self.comboBox.addItem("")
        self.gridContainer.addWidget(self.comboBox, 0, 0, 1, 1)
        self.keySearch = QLineEdit(widget)
        self.keySearch.setFocusPolicy(Qt.StrongFocus)
        self.keySearch.setStyleSheet("padding: 2 2 2 5;")
        self.keySearch.setObjectName("keySearch")
        self.gridContainer.addWidget(self.keySearch, 0, 1, 1, 1)
        main_layout.addWidget(widget)
        self.scrollArea = QScrollArea(add_app_dialog)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        main_layout.addWidget(self.scrollArea)

        self.retranslate_ui(add_app_dialog)
        QMetaObject.connectSlotsByName(add_app_dialog)

    def retranslate_ui(self, addAppDialog):
        _translate = QCoreApplication.translate
        addAppDialog.setWindowTitle(_translate("addAppDialog", "Dialog"))
        self.comboBox.setItemText(0, _translate("addAppDialog", "All repos"))
        self.keySearch.setPlaceholderText(_translate("addAppDialog", "Search apps"))

    def search_app(self):
        keyword = self.keySearch.text()
        if len(keyword) == 0:
            return
        docker_images = self.searchEngine.search(keyword, self.comboBox.currentText())
        self.load_result(docker_images)

    def load_result(self, docker_images):
        self.clean_search_results()
        for item in docker_images:
            widget = AddAppWidget(self.searchResultArea, item['name'], item['description'])
            self.searchResultArea.layout().addWidget(widget)

    def clean_search_results(self):
        while self.searchResultArea.layout().count():
            item = self.searchResultArea.layout().takeAt(0)
            item.widget().deleteLater()
