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

from boatswain.common.services import style_service
from boatswain.preferences.appearances.appearances_preferences_ui import AppearancesPreferencesUi
from boatswain.preferences.appearances.unit.appearance_unit import AppearanceUnit


class AppearancesPreferences:

    appearances = ['auto', 'dark', 'light']

    def __init__(self, parent) -> None:
        self.ui = AppearancesPreferencesUi(parent, self)
        for appearance in self.appearances:
            unit = AppearanceUnit(self.ui, style_service.getStyleFilePath(appearance))
            self.ui.horizontal_layout.addWidget(unit.ui)
