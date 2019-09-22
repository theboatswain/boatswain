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
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

import os

from docker.types import CancellableStream
from ctypes import Structure, c_int32, c_uint64, sizeof
from boatswain_updater.utils import sys_utils


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


class MemoryStatusEx(Structure):
    _fields_ = [
        ('length', c_int32),
        ('memoryLoad', c_int32),
        ('totalPhys', c_uint64),
        ('availPhys', c_uint64),
        ('totalPageFile', c_uint64),
        ('availPageFile', c_uint64),
        ('totalVirtual', c_uint64),
        ('availVirtual', c_uint64),
        ('availExtendedVirtual', c_uint64)]

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.length = sizeof(self)


def split_all(path):
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
    if sys_utils.isWin():
        from ctypes import windll, byref
        m = MemoryStatusEx()
        windll.kernel32.GlobalMemoryStatusEx(byref(m))
        return m.totalPhys / (1024. ** 2)
    else:
        mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')  # e.g. 4015976448
        return mem_bytes / (1024. ** 2)
