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

from boatswain_updater.models.app_to_update import AppToUpdate
from boatswain_updater.utils import sys_utils

from boatswain.common.utils import utils

current_dir = os.path.dirname(__file__)


def getResource(file):
    path = os.path.join(current_dir, file)
    return path


def getExternalResource(file):
    """
    This function will return the path to file in system resource folder after released.
    Depending on OS,
    For MacOS, the resource folder should be Boatswain.app/Contents/Resources
    For Window and Linux, resource folder should be the installed dir
    in debug mode, this will return the file in /resources folder
    @rtype: resource file name
    """
    if not utils.isFrost():
        return os.path.join(os.path.dirname(current_dir), "resources", file)
    original_app = AppToUpdate()
    if sys_utils.isMac():
        return os.path.join(original_app.folder, 'Contents', 'Resources', file)
    return os.path.join(original_app.folder, file)
