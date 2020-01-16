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

from boatswain.preferences.general.general_preferences_ui import GeneralPreferencesUi


class GeneralPreferences:

    def __init__(self, parent) -> None:
        self.ui = GeneralPreferencesUi(parent, self)
        # Todo: Terminals selection UI
        # Todo: Start with OS
        # Todo: Automatic check for updates
        # Todo: Language