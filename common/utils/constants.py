#  This file is part of Boatswain.
#
#      Boatswain is free software: you can redistribute it and/or modify
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
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#

from appdirs import *

APP_NAME = 'boatswain'
APP_AUTHOR = 'theboatswain'

APP_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
APP_LOG_DIR = user_log_dir(APP_NAME, APP_AUTHOR)

APP_DB = 'boatswain.db'

# Settings
INCLUDING_ENV_SYSTEM = 'including_env_system'
CONTAINER_CONF_CHANGED = 'container_conf_changed'

# Channels
CONTAINER_CHANNEL = 'container_channel'
APP_EXIT_CHANNEL = 'app_exit'
ADD_APP_CHANNEL = 'add_app_channel'
