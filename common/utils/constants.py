from appdirs import *

APP_NAME = 'boatswain'
APP_AUTHOR = 'theboatswain'

APP_DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)

APP_DB = 'boatswain.db'

# Settings
INCLUDING_ENV_SYSTEM = 'including_env_system'


# Channels
CONTAINER_CHANNEL = 'container_channel'
APP_EXIT_CHANNEL = 'app_exit'
ADD_APP_CHANNEL = 'add_app_channel'
