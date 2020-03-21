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

from boatswain.common.services import global_preference_service
from boatswain.common.utils import utils
from boatswain.common.utils.constants import DEFAULT_TERMINAL, AUTOMATIC_UPDATE, AUTOMATIC_FETCH_PREFERENCE_SHORTCUT
from boatswain.common.utils.utils import tr
from boatswain.preferences.general.general_preferences_ui import GeneralPreferencesUi


class GeneralPreferences:

    def __init__(self, parent) -> None:
        self.ui = GeneralPreferencesUi(parent, self)

        default_terminal = global_preference_service.getPreferenceValue(DEFAULT_TERMINAL)
        for item in utils.getListAvailableTerminals():
            self.ui.terminal.addItem(item['name'])
            if item['name'] == default_terminal:
                self.ui.terminal.setCurrentText(default_terminal)

        self.ui.check_for_update.setChecked(global_preference_service.isAutomaticUpdate())
        self.ui.check_for_update.stateChanged.connect(self.onAutoUpdateChanged)

        self.ui.fetch_shortcut.setChecked(global_preference_service.isAutomaticFetchPreferencesShortcuts())
        self.ui.fetch_shortcut.stateChanged.connect(self.onAutoFetchPreferenceShortcutChanged)

        self.ui.terminal.current_text_changed.connect(self.onTerminalChanged)
        self.ui.language.addItem(tr("English"))
        # Todo: Terminal open new tab if possible
        # Todo: Start with OS
        # Todo: Automatic fetch preferences shortcut
        # Todo: User set background image
        # Todo: Transparent
        # Todo: Language

    def onTerminalChanged(self, terminal):
        global_preference_service.setPreference(DEFAULT_TERMINAL, terminal)

    def onAutoUpdateChanged(self, status):
        global_preference_service.setPreference(AUTOMATIC_UPDATE, str(status))

    def onAutoFetchPreferenceShortcutChanged(self, status):
        global_preference_service.setPreference(AUTOMATIC_FETCH_PREFERENCE_SHORTCUT, str(status))
