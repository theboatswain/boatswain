from PyQt5.QtCore import QObject

from boatswain.common.services import style_service
from boatswain.preferences.appearances.unit.appearance_unit_ui import AppearanceUnitUi


class AppearanceUnit(QObject):

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
        style_service.activateTheme(theme_path)
