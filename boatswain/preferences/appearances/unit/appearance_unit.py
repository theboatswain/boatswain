from PyQt5.QtCore import QObject, pyqtSignal

from boatswain.common.services import style_service, global_preference_service
from boatswain.common.utils.constants import DEFAULT_SELECTION_COLOR, DEFAULT_FONT_COLOR, DEFAULT_BG_COLOR
from boatswain.preferences.appearances.unit.appearance_unit_ui import AppearanceUnitUi


class AppearanceUnit(QObject):

    theme_changed = pyqtSignal()

    def __init__(self, parent, theme_path) -> None:
        super().__init__(parent)
        self.theme_path = theme_path
        self.definition, self.variables = style_service.readTheme(theme_path)
        self.theme_name = style_service.getName(self.definition)
        self.ui = AppearanceUnitUi(parent, self.theme_name, self.definition, self)
        self.ui.selected.connect(self.onSelected)
        self.theme_name = self.theme_name

    def onSelected(self):
        if self.theme_name == 'Auto':
            theme_path = style_service.getStyleFilePath('base')
        else:
            theme_path = self.theme_path
        for key in [DEFAULT_BG_COLOR, DEFAULT_FONT_COLOR, DEFAULT_SELECTION_COLOR]:
            global_preference_service.removePreference(key)
        style_service.activateTheme(theme_path)
        self.theme_changed.emit()
