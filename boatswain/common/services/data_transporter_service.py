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

from typing import Dict, List

channels: Dict[str, List] = {}


def listen(channel: str, func):
    if channel in channels:
        channels[channel].append(func)
    else:
        channels[channel] = [func]


def deregister(channel: str, func):
    if channel in channels:
        try:
            channels[channel].remove(func)
        except ValueError:
            pass


def fire(channel: str, data=None):
    if channel in channels:
        for func in channels[channel]:
            if data is None:
                func()
            else:
                func(data)
