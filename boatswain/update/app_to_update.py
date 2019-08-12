import os
import sys

from boatswain.update.utils import permission_utils


class AppToUpdate:

    folder: str
    executable: str

    def __init__(self) -> None:
        self.executable = sys.executable
        (all_last_dir, folder) = os.path.split(self.executable)
        (all_before_last_dir, last_dir) = os.path.split(all_last_dir)
        (all_before_before_last_dir, before_last_dir) = os.path.split(all_before_last_dir)
        if last_dir == 'MacOS' and before_last_dir == 'Contents':
            self.folder = all_before_before_last_dir
        else:
            self.folder = all_last_dir

    def hasPermission(self):
        return permission_utils.locationIsWritable(self.folder)
