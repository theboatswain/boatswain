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
import os

from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QColorDialog, QPushButton, QFileDialog
from peewee import DoesNotExist

from boatswain import resources_utils
from boatswain.common.services import global_preference_service, data_transporter_service, style_service
from boatswain.common.utils.constants import WINDOW_COLOR_CHANNEL, DEFAULT_WINDOW_COLOR, \
    WINDOW_BG_CHANNEL, DEFAULT_WINDOW_IMG
from boatswain.common.utils.utils import tr
from boatswain.preferences.appearances.appearances_preferences_ui import AppearancesPreferencesUi
from boatswain.preferences.appearances.unit.appearance_unit import AppearanceUnit


class AppearancesPreferences:

    def __init__(self, parent) -> None:
        self.ui = AppearancesPreferencesUi(parent, self)
        self.ui.current_bg.clicked.connect(self.onSelectBgClicked)
        self.ui.select_bg.clicked.connect(self.onSelectBGImageClicked)
        window_color = global_preference_service.getPreferenceValue(DEFAULT_WINDOW_COLOR)
        if window_color:
            self.setColorButton(self.ui.current_bg, QColor(window_color))
        self.getListAppearances()

    def onSelectBgClicked(self):
        colour_dia = QColorDialog()
        selected_colour = colour_dia.getColor()
        global_preference_service.setPreference(DEFAULT_WINDOW_COLOR, selected_colour.name(QColor.HexRgb))
        data_transporter_service.fire(WINDOW_COLOR_CHANNEL, selected_colour)
        self.setColorButton(self.ui.current_bg, selected_colour)
        try:
            # When user changing window color, then remove image background (if exists)
            bg_img = global_preference_service.getPreference(DEFAULT_WINDOW_IMG)
            bg_img.delete_instance()
        except DoesNotExist:
            pass

    def onSelectBGImageClicked(self):
        fname = QFileDialog.getOpenFileName(self.ui, 'Select background image',
                                            filter=tr("Image Files (*.png *.jpg *.bmp *.svg)"))
        path = fname[0] if fname[0] else ''
        if path:
            global_preference_service.setPreference(DEFAULT_WINDOW_IMG, path)
            data_transporter_service.fire(WINDOW_BG_CHANNEL, path)

    def setColorButton(self, button: QPushButton, color: QColor):
        button.setText("")
        pal = button.palette()
        pal.setColor(QPalette.Button, color)
        button.setAutoFillBackground(True)
        button.setFlat(True)
        button.setPalette(pal)
        button.update()

    def getListAppearances(self):
        auto = AppearanceUnit(self.ui, style_service.getStyleFilePath("auto"))
        self.ui.horizontal_layout.addWidget(auto.ui)

        auto = AppearanceUnit(self.ui, style_service.getStyleFilePath("dark"))
        self.ui.horizontal_layout.addWidget(auto.ui)

        auto = AppearanceUnit(self.ui, style_service.getStyleFilePath("light"))
        self.ui.horizontal_layout.addWidget(auto.ui)
