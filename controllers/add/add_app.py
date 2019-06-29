import json
from PyQt5.QtCore import Qt, QCoreApplication, QMetaObject, QRect, QSize
from PyQt5.QtWidgets import QWidget, QSizePolicy, QVBoxLayout, QFrame, QScrollArea, QLineEdit, QComboBox, QGridLayout

from controllers.add.add_app_widget import AddAppWidget
from services.search.dockerhub_searcher import DockerHubSearcher
from services.search.search_images import DefaultSearchImages
from utils.custom_ui import BQSizePolicy


class AddAppDialog(object):

    def __init__(self, title, dialog) -> None:
        super().__init__()
        self.title = title
        self.setupUi(dialog)
        dialog.setWindowTitle(self.title)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        self.searchResultArea = QWidget(dialog)
        self.searchResultArea.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.searchResultArea.setLayout(QVBoxLayout(self.searchResultArea))
        self.searchResultArea.setContentsMargins(0, 0, 0, 0)
        self.scrollArea.setWidget(self.searchResultArea)
        self.keySearch.returnPressed.connect(self.searchApp)

        # Initialising search engines
        self.searchEngine = DefaultSearchImages()
        self.searchEngine = DockerHubSearcher(self.searchEngine)

        # Loading default search images
        with open('resources/default_search.json', 'r') as f:
            self.loadResult(json.load(f))

    def setupUi(self, addAppDialog):
        addAppDialog.resize(792, 387)
        addAppDialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        addAppDialog.setMinimumSize(QSize(792, 387))
        addAppDialog.setSizeGripEnabled(False)
        addAppDialog.setModal(False)
        mainLayout = QVBoxLayout(addAppDialog)
        mainLayout.setContentsMargins(8, 8, 8, 8)
        mainLayout.setSpacing(0)
        widget = QWidget(addAppDialog)
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
        mainLayout.addWidget(widget)
        self.scrollArea = QScrollArea(addAppDialog)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setWidgetResizable(True)
        mainLayout.addWidget(self.scrollArea)

        self.retranslateUi(addAppDialog)
        QMetaObject.connectSlotsByName(addAppDialog)

    def retranslateUi(self, addAppDialog):
        _translate = QCoreApplication.translate
        addAppDialog.setWindowTitle(_translate("addAppDialog", "Dialog"))
        self.comboBox.setItemText(0, _translate("addAppDialog", "All repos"))
        self.keySearch.setPlaceholderText(_translate("addAppDialog", "Search apps"))

    def searchApp(self):
        keyword = self.keySearch.text()
        if len(keyword) == 0:
            return
        docker_images = self.searchEngine.search(keyword, self.comboBox.currentText())
        self.loadResult(docker_images)

    def loadResult(self, docker_images):
        self.cleanSearchResults()
        for item in docker_images:
            widget = AddAppWidget(self.searchResultArea, item['name'], item['description'])
            self.searchResultArea.layout().addWidget(widget)

    def cleanSearchResults(self):
        while self.searchResultArea.layout().count():
            item = self.searchResultArea.layout().takeAt(0)
            item.widget().deleteLater()
