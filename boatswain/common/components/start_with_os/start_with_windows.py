import os
import sys

from boatswain.common.components.start_with_os.start_with_os import StartWithOS
from boatswain.common.utils.constants import USER_NAME


class StartWithWindows(StartWithOS):

    startup_file = '~/.xinitrc'

    def isEnabled(self):
        return os.path.isfile(self.startup_file)

    def enableStartWithOS(self):
        with open(self.startup_file, "a") as bat_file:
            bat_file.write('\nexec %s\n' % sys.executable)

    def disableStartWithOS(self):
        os.remove(self.startup_file)
