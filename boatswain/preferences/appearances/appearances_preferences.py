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
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject
from PyQt5.QtGui import QColor

from boatswain.common.services import style_service, global_preference_service
from boatswain.common.utils.constants import DEFAULT_BG_COLOR, DEFAULT_FONT_COLOR, DEFAULT_SELECTION_COLOR
from boatswain.common.utils.utils import tr
from boatswain.preferences.appearances.appearances_preferences_ui import AppearancesPreferencesUi
from boatswain.preferences.appearances.unit.appearance_unit import AppearanceUnit


class AppearancesPreferences(QObject):

    appearances = ['auto', 'dark', 'light']

    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.ui = AppearancesPreferencesUi(parent, self)
        for appearance in self.appearances:
            unit = AppearanceUnit(self.ui, style_service.getStyleFilePath(appearance))
            self.ui.horizontal_layout.addWidget(unit.ui)
            unit.theme_changed.connect(self.setColors)
        self.buttons = {
            self.ui.bg_color: DEFAULT_BG_COLOR,
            self.ui.font_color: DEFAULT_FONT_COLOR,
            self.ui.selection_color: DEFAULT_SELECTION_COLOR
        }
        for button in self.buttons:
            button.clicked.connect(self.onSelectColorClicked)
        self.setColors()

    def setColors(self):
        if not style_service.isAutoThemeActivating():
            for button in self.buttons:
                button.setText("")
                color = self.getPreference(self.buttons[button])
                self.setColorButton(button, color)
        else:
            color = "#999999"
            for button in self.buttons:
                button.setText(tr("Auto"))
                self.setColorButton(button, color)

    def onSelectColorClicked(self):
        if style_service.isAutoThemeActivating():
            return
        button = self.sender()
        color = self.getPreference(self.buttons[button])
        colour_dia = QtWidgets.QColorDialog()
        selected_colour = colour_dia.getColor(QColor(color))
        if selected_colour.isValid():
            self.setColorButton(button, selected_colour.name())
            global_preference_service.setPreference(self.buttons[button], selected_colour.name())
            style_service.reloadTheme()

    def setColorButton(self, button: QObject, color):
        if color is not None:
            button.setStyleSheet("background-color: " + color)
            button.update()

    def getPreference(self, key):
        background_color = global_preference_service.getPreferenceValue(key)
        if not background_color:
            background_color = global_preference_service.getInMemoryPreferences(key)
        return background_color
