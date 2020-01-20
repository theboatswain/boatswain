import os
import re

from peewee import DoesNotExist

from boatswain import resources_utils
from boatswain.common.services import global_preference_service
from boatswain.common.utils import file_utils
from boatswain.common.utils.constants import DEFAULT_THEME


def getName(style_content):
    for line in style_content.splitlines():
        name_search = re.search(r'^\s*Name:\s+(.*)$', line)
        if name_search:
            return name_search.group(1)
    return "No name"


def getStyleFilePath(name):
    return resources_utils.getExternalResource(os.path.join('appearances', '%s.qss' % name))


def getCurrentActivatedStyle():
    try:
        default_path = global_preference_service.getPreference(DEFAULT_THEME)
        return file_utils.readFile(default_path.value)
    except DoesNotExist:
        return resources_utils.getExternalResourceAsString(getStyleFilePath('base'))
