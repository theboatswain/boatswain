import platform
from time import strftime, gmtime

import yaml
from playhouse.shortcuts import model_to_dict

from boatswain.common.models.container import Container
from boatswain.common.models.preferences_shortcut import PreferencesShortcut
from boatswain.common.services import shortcut_service


class ShortcutYaml(yaml.YAMLObject):
    yaml_tag = u'!ShortcutYAML'
    image_name: str
    repo: str
    author: str
    email: str
    release_date: str
    shortcuts = []

    def __init__(self, image_name, repo, shortcuts) -> None:
        super().__init__()
        self.image_name = image_name
        self.repo = repo
        self.shortcuts = shortcuts
        self.author = platform.node()
        self.email = ''
        self.release_date = strftime("%Y-%m-%dT%H:%M:%S", gmtime())

    @staticmethod
    def build(container: Container):
        shortcuts = []
        for shortcut in shortcut_service.getShortcuts(container):
            shortcut_dict = model_to_dict(shortcut, recurse=False,
                                          exclude=[PreferencesShortcut.container, PreferencesShortcut.id])
            shortcuts.append(shortcut_dict)
        return ShortcutYaml(container.image_name, container.repo, shortcuts)

    def toYAML(self):
        return yaml.dump(self, default_flow_style=False)

    @staticmethod
    def fromYaml(yaml_str: str):
        return yaml.load(yaml_str, Loader=yaml.Loader)
