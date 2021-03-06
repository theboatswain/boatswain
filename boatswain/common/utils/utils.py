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
import subprocess
from contextlib import closing

from PyQt5.QtCore import QFile

from boatswain_updater.utils import sys_utils
from docker.types import CancellableStream

total_mem = None


class EmptyStream(CancellableStream):

    def __init__(self):
        super().__init__(None, None)

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    next = __next__

    def close(self):
        pass


def splitAll(path):
    all_parts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            all_parts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            all_parts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            all_parts.insert(0, parts[1])
    return all_parts


def disconnectAllSignals(widget):
    try:
        widget.disconnect()
    except TypeError:
        return


def getPhysicalMemory():
    global total_mem
    if total_mem:
        return total_mem / (1024. ** 2)
    if sys_utils.isWin():
        res = subprocess.run(['wmic', 'ComputerSystem', 'get', 'TotalPhysicalMemory'], stdout=subprocess.PIPE)
        output = res.stdout.decode('utf-8')
        total = int(output.replace('TotalPhysicalMemory', '').strip())
    elif sys_utils.isLinux():
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
        total = mem_bytes
    else:
        res = subprocess.run(['sysctl', '-n', 'hw.memsize'], stdout=subprocess.PIPE)
        output = res.stdout.decode('utf-8')
        total = int(output.strip())
    total_mem = total
    return total / (1024. ** 2)


def isFrost():
    with closing(QFile(':/certifi/cacert.pem')) as frozen_file:
        if frozen_file.open(QFile.ReadOnly):
            return True
    return False
