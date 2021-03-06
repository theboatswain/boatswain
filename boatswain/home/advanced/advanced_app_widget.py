#  This file is part of Boatswain.
#
#      Boatswain<https://github.com/theboatswain> is free software: you can redistribute it and/or modify
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
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5.QtCore import QPropertyAnimation, QCoreApplication
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QLabel, QComboBox, QSizePolicy, QWidget, QLineEdit, QPushButton, QFileDialog

from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.services import containers_service, shortcut_service, tags_service, auditing_service
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy
from boatswain.common.ui.path_view import PathViewWidget
from boatswain.common.utils.constants import SHORTCUT_CONF_CHANGED_CHANNEL
from boatswain.config.app_config import AppConfig
from boatswain.home.advanced.advanced_app_widget_ui import AdvancedAppWidgetUi


class AdvancedAppWidget:
    _translate = QCoreApplication.translate
    template = 'AdvancedAppWidget'
    animation: QPropertyAnimation
    tags: QComboBox

    def __init__(self, parent, container: Container) -> None:
        self.container = container
        self.ui = AdvancedAppWidgetUi(parent, container)
        self.drawShortcuts()
        containers_service.listen(self.container, 'tag_index', self.listenTagChange)
        containers_service.listen(self.container, SHORTCUT_CONF_CHANGED_CHANNEL, self.redrawShortcuts)
        if not container.expanded:
            self.ui.setMaximumHeight(0)
        self.ui.resizeEvent = self.resize

    def onImageTagChange(self, full_tag_name):
        if not full_tag_name:
            return
        tag = full_tag_name.split(':')[1]
        previous_val = self.container.tag
        self.container.tag = tag
        self.container.save()
        auditing_service.audit_update(self.container, self.container.tableName(), self.container.id, "tag",
                                      previous_val, tag)

    def onAdvancedConfigurationClicked(self):
        app_config = AppConfig(None, self.container)
        app_config.show()

    def onCollapsed(self):
        self.container.expanded = False
        self.container.save()

    def onExpanded(self):
        self.container.expanded = True
        self.container.save()
        self.ui.setMaximumHeight(99999)

    def toggleWindow(self):
        self.animation = QPropertyAnimation(self.ui, b"maximumHeight")
        self.animation.setDuration(200)
        try:
            self.animation.finished.disconnect()
        except TypeError:
            pass
        if self.ui.maximumHeight() == 0:
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.ui.layout.sizeHint().height())
            self.animation.finished.connect(self.onExpanded)
        else:
            self.animation.setStartValue(self.ui.layout.sizeHint().height())
            self.animation.setEndValue(0)
            self.animation.finished.connect(self.onCollapsed)
        self.animation.start()

    def findFileOrFolder(self, shotcut: PreferencesShortcut, input_box: PathViewWidget):
        if shotcut.pref_type == 'File':
            fname = QFileDialog.getOpenFileName(self.ui, 'Open file')
            path = fname[0] if fname[0] else ''
        else:
            file = str(QFileDialog.getExistingDirectory(self.ui, "Select Directory"))
            path = file if file else ''
        if path:
            input_box.setPath(path, shotcut.pref_type.lower())
            input_box.resizePaths()
            self.setShortcutValue(shotcut, path)

    def drawShortcut(self, shortcut: PreferencesShortcut, row):
        label = QLabel(self.ui.widget)
        label.setText(self._translate(self.template, shortcut.label) + ':')
        label.setToolTip(shortcut.description)
        self.ui.grid_layout.addWidget(label, row, 0, 1, 1)
        if shortcut.pref_type in ['File', 'Folder']:
            input_box = PathViewWidget(self.ui.widget)
            input_box.setPath(shortcut.default_value, shortcut.pref_type.lower())
            self.ui.grid_layout.addWidget(input_box, row, 1, 1, 2)
            finder = QPushButton(self.ui.widget)
            finder.setText(' ... ')
            finder.setFlat(True)
            finder.setStyleSheet("border: 1px solid #999999; padding: 0px 4px; border-radius: 2px")
            finder.setMaximumWidth(rt(25))
            finder.clicked.connect(lambda x: self.findFileOrFolder(shortcut, input_box))
            self.ui.grid_layout.addWidget(finder, row, 3, 1, 2)
        else:
            input_box = QLineEdit(self.ui.widget)
            input_box.setText(shortcut.default_value)
            input_box.textChanged.connect(lambda x: self.setShortcutValue(shortcut, x))
            input_box.setStyleSheet('border: none; background-color: transparent')
            input_box.setReadOnly(shortcut.shortcut == 'Constant')
            self.ui.grid_layout.addWidget(input_box, row, 1, 1, 2)
            hidden_widget = QWidget(self.ui.widget)
            hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
            self.ui.grid_layout.addWidget(hidden_widget, row, 3, 1, 2)

    def drawTagShortcut(self, row):
        label = QLabel(self.ui.widget)
        self.ui.grid_layout.addWidget(label, row, 0, 1, 1)
        self.tags = QComboBox(self.ui.widget)
        self.tags.setSizePolicy(BQSizePolicy(h_stretch=4, height=QSizePolicy.Fixed, width=QSizePolicy.Fixed))
        self.ui.grid_layout.addWidget(self.tags, row, 1, 1, 2)
        hidden_widget = QWidget(self.ui.widget)
        hidden_widget.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.ui.grid_layout.addWidget(hidden_widget, row, 3, 1, 2)

        for index, tag in enumerate(tags_service.getTags(self.container)):
            self.tags.addItem(self.container.image_name + ":" + tag.name)
            if tag.name == self.container.tag:
                self.tags.setCurrentIndex(index)
        self.tags.currentTextChanged.connect(self.onImageTagChange)
        label.setText(self._translate(self.template, "Image tag:"))

    def drawShortcuts(self):
        shortcuts = shortcut_service.getEnabledShortcuts(self.container)
        for index, shortcut in enumerate(shortcuts):
            self.drawShortcut(shortcut, index)
        self.drawTagShortcut(len(shortcuts))

    def cleanShortcuts(self):
        while self.ui.grid_layout.count():
            item = self.ui.grid_layout.takeAt(0)
            item.widget().deleteLater()

    def redrawShortcuts(self):
        self.cleanShortcuts()
        self.drawShortcuts()

    def listenTagChange(self, index):
        self.tags.setCurrentIndex(index)

    def setShortcutValue(self, shortcut: PreferencesShortcut, value):
        previous_val = shortcut.default_value
        shortcut.default_value = value
        shortcut.save()
        auditing_service.audit_update(self.container, shortcut.tableName(), shortcut.id, "default_value",
                                      previous_val, value)

    def resize(self, event: QResizeEvent):
        if self.tags:
            self.tags.setFixedWidth(event.size().width() * 2 / 3)
        QWidget.resizeEvent(self.ui, event)
