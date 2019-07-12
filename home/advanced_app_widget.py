from PyQt5.QtCore import QMetaObject, QCoreApplication, pyqtSlot
from PyQt5.QtWidgets import QWidget, QSizePolicy, QPushButton, QLabel, QComboBox, QFrame, QVBoxLayout, \
    QHBoxLayout

from common.models.container import Container
from common.models.tag import Tag
from common.utils.custom_ui import BQSizePolicy


class AdvancedAppWidget(QWidget):

    def __init__(self, parent, container: Container) -> None:
        super().__init__(parent)
        self.container = container
        self.setSizePolicy(BQSizePolicy(height=QSizePolicy.Fixed))
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 0, 3, 0)
        self.layout.setSpacing(6)
        line = QFrame(self)
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)
        self.widget = QWidget(self)
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(6)
        self.label = QLabel(self.widget)
        self.horizontal_layout.addWidget(self.label)
        self.tags = QComboBox(self.widget)
        self.tags.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.tags.setObjectName("tags")
        self.horizontal_layout.addWidget(self.tags)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout.addWidget(self.widget_2)
        self.layout.addWidget(self.widget)
        self.widget_3 = QWidget(self)
        self.horizontal_layout_2 = QHBoxLayout(self.widget_3)
        self.horizontal_layout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout_2.setSpacing(6)
        self.widget_4 = QWidget(self.widget_3)
        self.widget_4.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontal_layout_2.addWidget(self.widget_4)
        self.advanced_configuration = QPushButton(self.widget_3)
        self.advanced_configuration.setObjectName("advancedConfiguration")
        self.horizontal_layout_2.addWidget(self.advanced_configuration)
        self.layout.addWidget(self.widget_3)

        self.retranslateUi()
        QMetaObject.connectSlotsByName(self)

        for index, tag in enumerate(Tag.select().where(Tag.container == container)):
            self.tags.addItem(container.image_name + ":" + tag.name)
            if tag.name == container.tag:
                self.tags.setCurrentIndex(index)
        self.tags.currentIndexChanged.connect(self.onImageTagChange)

    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.label.setText(_translate("AdvancedWidget", "Image tag:"))
        self.advanced_configuration.setText(_translate("AdvancedWidget", "Advanced configuration"))

    def onImageTagChange(self, index):
        tag = self.tags.itemText(index).split(':')[1]
        self.container.tag = tag
        self.container.container_id = ""
        self.container.save()
        # Todo: Should we do the clean up? delete the downloaded image
