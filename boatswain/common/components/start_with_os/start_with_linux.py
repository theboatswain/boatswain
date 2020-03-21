import os
import sys

from boatswain.common.components.start_with_os.start_with_os import StartWithOS
from boatswain.common.utils.constants import USER_NAME


class StartWithWindows(StartWithOS):

    startup_dir = 'C:\\Users\\%s\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup' % USER_NAME
    startup_file = '%s\\boatswain.bat' % startup_dir

    def isEnabled(self):
        return os.path.isfile(self.startup_file)

    def enableStartWithOS(self):
        with open(self.startup_file) as bat_file:
            bat_file.write('start "" %s' % sys.executable)

    def disableStartWithOS(self):
        os.remove(self.startup_file)
