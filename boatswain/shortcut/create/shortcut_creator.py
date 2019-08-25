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
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QWidget, QToolTip, QMessageBox, QFileDialog

from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.services import containers_service, config_service
from boatswain.common.utils.constants import SHORTCUT_CONF_CHANGED_CHANNEL, CONTAINER_CONF_CHANGED
from boatswain.shortcut.create.shortcut_creator_ui import ShortcutCreatorUi


class ShortcutCreator:
    _translate = QtCore.QCoreApplication.translate
    template = 'PreferenceShortcut'
    shortcut_types = ['Volume Mount', 'Port Mapping', 'Environment']
    data_types = ['String', 'Folder', 'File', 'Number']

    def __init__(self, container: Container, widget: QWidget, shortcut: PreferencesShortcut) -> None:
        self.dialog = QDialog(widget)
        self.container = container
        self.ui = ShortcutCreatorUi(self.dialog, container)
        self.dialog.ui = self.ui
        self.retranslateUi()
        self.ui.container_name.addItem(container.name)
        self.ui.container_name.setDisabled(True)
        for shortcut_type in self.shortcut_types:
            self.ui.shortcut_type.addItem(shortcut_type)
            if shortcut_type == shortcut.shortcut:
                self.ui.shortcut_type.setCurrentText(shortcut_type)
        for data_type in self.data_types:
            self.ui.data_type.addItem(data_type)
            if data_type == shortcut.pref_type:
                self.ui.data_type.setCurrentText(data_type)
        self.ui.mapping_to.setText(shortcut.mapping_to)
        self.ui.default_value.setText(shortcut.default_value)
        self.shortcut = shortcut
        self.ui.shortcut_label.setText(shortcut.label)
        self.dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.ui.next_button.clicked.connect(self.next)
        self.ui.back_button.clicked.connect(lambda x: self.ui.stacked_widget.setCurrentIndex(0))
        self.ui.shortcut_type.currentTextChanged.connect(self.onShortcutTypeChange)
        self.ui.data_type.currentTextChanged.connect(self.onDatatypeChange)
        self.ui.finish_button.clicked.connect(self.finish)
        self.ui.cancel_button.clicked.connect(self.cancel)
        self.ui.cancel_button_2.clicked.connect(self.cancel)
        self.ui.default_value.button_clicked.connect(self.onFindDirClicked)
        if shortcut.pref_type in ['File', 'Folder']:
            self.ui.default_value.button.setVisible(True)

    def show(self):
        return self.dialog.exec_()

    def cancel(self):
        button_reply = QMessageBox.question(self.dialog, 'Preference shortcut', "Are you sure?",
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
        if button_reply == QMessageBox.Ok:
            self.dialog.close()

    def next(self):
        if not self.ui.shortcut_label.text():
            message = self._translate(self.template, 'Label can not be empty')
            QToolTip.showText(self.ui.shortcut_label.mapToGlobal(QPoint()), message)
            return
        if self.ui.shortcut_type.currentText() == 'Port Mapping':
            self.ui.mapping_to.setValidator(QIntValidator(0, 9999999))
        else:
            self.ui.mapping_to.setValidator(None)
        self.describeValues()
        self.ui.stacked_widget.setCurrentIndex(1)

    def isCreateMode(self):
        return self.shortcut.label is None

    def finish(self):
        if not self.ui.mapping_to.text():
            message = self._translate(self.template, 'The value of \'Mapping to\' can not be empty')
            QToolTip.showText(self.ui.mapping_to.mapToGlobal(QPoint()), message)
            return
        shortcut_type = self.ui.shortcut_type.currentText()
        mapping_to = self.ui.mapping_to.text()

        # Is create mode
        if self.isCreateMode() and self.findShortcut(self.container, shortcut_type, mapping_to):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)

            msg.setText(self._translate(self.template, "Preference shortcut already exists!!!"))
            msg.setInformativeText('Preference shortcut with type: %s, mapping to: %s is already exist!\n\n'
                                   'Please choose another one' % (shortcut_type, mapping_to))
            msg.setStandardButtons(QMessageBox.Ok)
            return msg.exec_()

        if self.isCreateMode():
            order = PreferencesShortcut.select().where(PreferencesShortcut.container == self.container).count() * 10000
            self.shortcut.order = order

        self.shortcut.container = self.container
        self.shortcut.label = self.ui.shortcut_label.text()
        self.shortcut.default_value = self.ui.default_value.text()
        self.shortcut.pref_type = self.ui.data_type.currentText()
        self.shortcut.shortcut = self.ui.shortcut_type.currentText()
        self.shortcut.mapping_to = self.ui.mapping_to.text()

        self.shortcut.save()
        config_service.setAppConf(self.shortcut.container, CONTAINER_CONF_CHANGED, 'true')
        containers_service.fire(self.container, SHORTCUT_CONF_CHANGED_CHANNEL, True)
        self.dialog.accept()

    def onShortcutTypeChange(self, shortcut_type):
        if shortcut_type == 'Port Mapping':
            self.ui.data_type.setCurrentText('Number')
            self.ui.data_type.setDisabled(True)
        else:
            self.ui.data_type.setCurrentText('String')
            self.ui.data_type.setDisabled(False)

    def findShortcut(self, container, shortcut_type, mapping_to):
        condition = (PreferencesShortcut.container == container) & (PreferencesShortcut.shortcut == shortcut_type)
        condition = condition & (PreferencesShortcut.mapping_to == mapping_to)
        return PreferencesShortcut.select().where(condition)

    def onFindDirClicked(self, arg):
        if self.ui.data_type.currentText() == 'File':
            fname = QFileDialog.getOpenFileName(self.dialog, 'Open file')
            if fname[0]:
                self.ui.default_value.setText(fname[0])
        elif self.ui.data_type.currentText() == 'Folder':
            file = str(QFileDialog.getExistingDirectory(self.dialog, "Select Directory"))
            if file:
                self.ui.default_value.setText(file)

    def onDatatypeChange(self, data_type):
        if data_type == 'Number':
            self.ui.default_value.setValidator(QIntValidator(0, 9999999))
        else:
            self.ui.default_value.setValidator(None)
        if data_type not in ['Folder', 'File', 'File & Folder']:
            self.ui.default_value.button.setVisible(False)
        else:
            self.ui.default_value.button.setVisible(True)

    def describeValues(self):
        if self.ui.shortcut_type.currentText() == 'Environment':
            self.ui.default_value_des.setText(self._translate(
                self.template, "The default value of this preference shortcut environment, "
                               "which the environment key in 'Mapping to' will point to. "
                               "When the container is being start, this environment will be set inside of it. \n"
                               "This value can be changed in the expanding window."))
            self.ui.mapping_to_des.setText(self._translate(
                self.template, "The key of this preference shortcut environment. \n"
                               "i.e MYSQL_PASSWORD. \n"
                               "This value can't be changed in the expanding window."))
        elif self.ui.shortcut_type.currentText() == 'Port Mapping':
            self.ui.default_value_des.setText(self._translate(
                self.template, "The default host port number of this preference shortcut port mapping, "
                               "which will be mapped into the container port described in the 'Mapping to' section. \n"
                               "This value can be changed in the expanding window."))
            self.ui.mapping_to_des.setText(self._translate(
                self.template, "The container port number of this preference shortcut port mapping. \n"
                               "This value can't be changed in the expanding window."))

        elif self.ui.shortcut_type.currentText() == 'Volume Mount':
            self.ui.default_value_des.setText(self._translate(
                self.template, "The default path to the shared folder of host machine, "
                               "which will be mount to the container folder described in the 'Mapping to' section. \n"
                               "The mount type will be read-write by default. \n"
                               "This value can be changed in the expanding window."))
            self.ui.mapping_to_des.setText(self._translate(
                self.template, "The container folder of this preference shortcut port mapping. \n"
                               "i.e /usr/share/nginx/html \n"
                               "This value can't be changed in the expanding window."))

    def retranslateUi(self):
        self.dialog.setWindowTitle(self._translate(self.template, "Preference Shortcut"))
        self.ui.shortcut_label.setPlaceholderText(self._translate(self.template, "i.e Root dir"))
        self.ui.data_type_label.setText(self._translate(self.template, "Datatype:"))
        self.ui.label_des.setText(self._translate(self.template, "Label will be appeared in the expanding window "
                                                                 "to let you know the meaning of this preference"))
        self.ui.type_label.setText(self._translate(self.template, "Shortcut type:"))
        self.ui.shortcut_for_des.setText(
            self._translate(self.template, "This preference shortcut will be applied to the specified application"))
        self.ui.shortcut_for_label.setText(self._translate(self.template, "Preference shortcut for:"))
        self.ui.label.setText(self._translate(self.template, "Label:"))
        self.ui.data_type_des.setText(self._translate(self.template, "Type of the input data, we will decide which "
                                                                     "kind of input element in the expanding window "
                                                                     "based on this information"))
        self.ui.cancel_button.setText(self._translate(self.template, "Cancel"))
        self.ui.next_button.setText(self._translate(self.template, "Next"))

        self.ui.tab_widget.setTabText(self.ui.tab_widget.indexOf(self.ui.tab),
                                      self._translate(self.template, "Create new preference shortcut"))
        self.ui.mapping_to_label.setText(self._translate(self.template, "Mapping to:"))
        self.ui.default_value_label.setText(self._translate(self.template, "Default value:"))
        self.ui.back_button.setText(self._translate(self.template, "Back"))
        self.ui.cancel_button_2.setText(self._translate(self.template, "Cancel"))
        self.ui.finish_button.setText(self._translate(self.template, "Finish"))
        self.ui.tab_widget_2.setTabText(self.ui.tab_widget_2.indexOf(self.ui.tab_3),
                                        self._translate(self.template, "Create new preference shortcut"))
