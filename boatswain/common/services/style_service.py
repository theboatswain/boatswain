import os
import re

from peewee import DoesNotExist

from boatswain import resources_utils
from boatswain.common.services import global_preference_service, data_transporter_service
from boatswain.common.utils import file_utils
from boatswain.common.utils.constants import DEFAULT_THEME, THEME_UPDATING_CHANNEL


def getName(style_content):
    for line in style_content.splitlines():
        name_search = re.search(r'^\s*Name:\s+(.*)$', line)
        if name_search:
            return name_search.group(1)
    return "No name"


def getStyleFilePath(name):
    return resources_utils.getExternalResource(os.path.join('appearances', '%s.qss' % name))


def readTheme(file_path):
    """
    Read theme file and replace the content with its variables
    @rtype: str, dict
    """
    theme_content = file_utils.readFile(file_path)
    variables = {}
    for line in theme_content.splitlines():
        key_search = re.search(r'^\s*(@[A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9()#, ]+)$', line)
        if key_search:
            variables[key_search.group(1)] = key_search.group(2)

    for key in variables:
        theme_content = theme_content.replace(key, variables[key])
    return theme_content, variables


def activateTheme(theme_path):
    global_preference_service.setPreference(DEFAULT_THEME, theme_path)
    theme, variables = readTheme(theme_path)
    for key in variables:
        global_preference_service.setInMemoryPreferences(key, variables[key])
    data_transporter_service.fire(THEME_UPDATING_CHANNEL, theme)
    return theme


def getCurrentActivatedThemePath():
    try:
        default_path = global_preference_service.getPreference(DEFAULT_THEME)
        return default_path.value
    except DoesNotExist:
        return getStyleFilePath('base')
