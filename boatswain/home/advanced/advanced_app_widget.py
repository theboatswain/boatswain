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
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5.QtCore import QPropertyAnimation, QCoreApplication
from PyQt5.QtWidgets import QLabel, QComboBox, QSizePolicy, QWidget, QLineEdit, QPushButton, QFileDialog

from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.models.tag import Tag
from boatswain.common.services import config_service, containers_service
from boatswain.common.utils.constants import CONTAINER_CONF_CHANGED
from boatswain.common.utils.custom_ui import BQSizePolicy
from boatswain.config.app_config import AppConfig
from boatswain.home.advanced.advanced_app_widget_ui import AdvancedAppWidgetUi


class AdvancedAppWidget:
    _translate = QCoreApplication.translate
    template = 'AdvancedAppWidget'
    animation: QPropertyAnimation
    tags: QComboBox
    app_info_max_height: int

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = AdvancedAppWidgetUi(parent, container)
        self.ui.advanced_configuration.clicked.connect(self.onAdvancedConfigurationClicked)
        self.drawShortcuts()
        containers_service.listen(self.container, 'tag_index', self.listenTagChange)

    def onImageTagChange(self, full_tag_name):
        if not full_tag_name:
            return
        tag = full_tag_name.split(':')[1]
        self.container.tag = tag
        self.container.save()
        config_service.setAppConf(self.container, CONTAINER_CONF_CHANGED, 'true')
        # Todo: Should we do the clean up? delete the downloaded image

    def onAdvancedConfigurationClicked(self):
        app_config = AppConfig(self.ui, self.container)
        app_config.show()

    def toggleWindow(self):
        if self.ui.maximumHeight() == 0:
            self.animation = QPropertyAnimation(self.ui, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.app_info_max_height)
            self.animation.start()
        else:
            self.animation = QPropertyAnimation(self.ui, b"maximumHeight")
            self.animation.setDuration(300)
            self.animation.setStartValue(self.app_info_max_height)
            self.animation.setEndValue(0)
            self.animation.start()

    def findFileOrFolder(self, shotcut: PreferencesShortcut, input_box: QLineEdit):
        if shotcut.pref_type == 'File':
            fname = QFileDialog.getOpenFileName(self.ui, 'Open file')
            path = fname[0] if fname[0] else ''
        else:
            file = str(QFileDialog.getExistingDirectory(self.ui, "Select Directory"))
            path = file if file else ''
        if path:
            input_box.setText(path)

    def drawShortcut(self, shortcut: PreferencesShortcut, row):
        label = QLabel(self.ui.widget)
        label.setText(self._translate(self.template, shortcut.label) + ':')
        self.ui.grid_layout.addWidget(label, row, 0, 1, 1)
        input_box = QLineEdit(self.ui.widget)
        input_box.setText(shortcut.default_value)
        input_box.setStyleSheet('border: none; background-color: transparent')
        self.ui.grid_layout.addWidget(input_box, row, 1, 1, 2)
        if shortcut.pref_type in ['File', 'Folder']:
            finder = QPushButton(self.ui.widget)
            finder.setText('...')
            finder.setMaximumWidth(40)
            finder.clicked.connect(lambda x: self.findFileOrFolder(shortcut, input_box))
            self.ui.grid_layout.addWidget(finder, row, 3, 1, 2)
        else:
            hidden_widget = QWidget(self.ui.widget)
            hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
            self.ui.grid_layout.addWidget(hidden_widget, row, 3, 1, 2)

    def drawTagShortcut(self, row):
        label = QLabel(self.ui.widget)
        self.ui.grid_layout.addWidget(label, row, 0, 1, 1)
        self.tags = QComboBox(self.ui.widget)
        self.tags.setSizePolicy(BQSizePolicy(h_stretch=2, height=QSizePolicy.Fixed))
        self.ui.grid_layout.addWidget(self.tags, row, 1, 1, 2)
        hidden_widget = QWidget(self.ui.widget)
        hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.ui.grid_layout.addWidget(hidden_widget, row, 3, 1, 2)

        for index, tag in enumerate(Tag.select().where(Tag.container == self.container)):
            self.tags.addItem(self.container.image_name + ":" + tag.name)
            if tag.name == self.container.tag:
                self.tags.setCurrentIndex(index)
        self.tags.currentTextChanged.connect(self.onImageTagChange)
        label.setText(self._translate(self.template, "Image tag:"))

    def drawShortcuts(self):
        shortcuts = PreferencesShortcut.select().where(PreferencesShortcut.container == self.container)
        for index, shortcut in enumerate(shortcuts):
            self.drawShortcut(shortcut, index)
        self.drawTagShortcut(len(shortcuts))

        is_collapsed = self.ui.maximumHeight() == 0
        self.ui.setMaximumHeight(9999999)
        self.app_info_max_height = self.ui.sizeHint().height() + 10
        if is_collapsed:
            self.ui.setMaximumHeight(0)
        else:
            self.ui.setMaximumHeight(self.app_info_max_height)

    def cleanShortcuts(self):
        while self.ui.grid_layout.count():
            item = self.ui.grid_layout.takeAt(0)
            item.widget().deleteLater()

    def redrawShortcuts(self):
        self.cleanShortcuts()
        self.drawShortcuts()

    def listenTagChange(self, index):
        self.tags.setCurrentIndex(index)
