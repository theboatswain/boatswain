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

from appdirs import user_data_dir, user_log_dir

APP_NAME = 'boatswain'
APP_AUTHOR = 'theboatswain'

APP_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
APP_LOG_DIR = user_log_dir(APP_NAME, APP_AUTHOR)
APP_AVATAR_DIR = os.path.join(APP_DATA_DIR, "avatars")

PEM_FILE = os.path.join(APP_DATA_DIR, "cacert.pem")
DEFAULT_SEARCH_APP_FILE = os.path.join(APP_DATA_DIR, "default_search.json")

APP_DB = 'boatswain.db'

# Settings
INCLUDING_ENV_SYSTEM = 'including_env_system'
CURRENT_ACTIVATED_WORKSPACE = 'current_activated_workspace'

# Channels
CONTAINER_CHANNEL = 'container_channel'
APP_EXIT_CHANNEL = 'app_exit'
ADD_APP_CHANNEL = 'add_app_channel'
CONTAINER_CONF_CHANGED_CHANNEL = 'container_conf_channel'
SHORTCUT_CONF_CHANGED_CHANNEL = 'shortcut_conf_channel'
UPDATES_CHANNEL = 'check_for_updates'

# Docker
WINDOWS_BASE_URL = 'tcp://127.0.0.1:2375'
UNIX_BASE_URL = 'unix://var/run/docker.sock'


# Global conf
HOME_WIDTH = 'home_width'
HOME_HEIGHT = 'home_height'
DEFAULT_SEARCH_UPDATE_DATE = 'default_search_update_date'


# Other conf
SEARCH_APP_WIDTH = 275
DEFAULT_CONTAINERS = ['nginx', 'ubuntu', 'mysql', 'node', 'redis', 'postgres', 'mongo', 'jenkins',
                      'elasticsearch', 'wordpress', 'mariadb', 'memcached', 'tomcat', 'rabbitmq', 'django', 'arangodb']

STATUS_DELETED = 0
STATUS_ADDED = 1

AUDIT_CREATE = "Create"
AUDIT_DELETE = "Delete"
