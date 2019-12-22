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

import logging
import os
import sys

from boatswain_updater.utils import sys_utils

from boatswain.common.utils.constants import APP_LOG_DIR

log_file = os.path.join(APP_LOG_DIR, 'boatswain.log')
if not os.path.isdir(APP_LOG_DIR):
    os.makedirs(APP_LOG_DIR)


logger = logging.getLogger('boatswain')
logger.setLevel(logging.INFO)
# create file handler which logs even debug messages
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', "%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(fh)


class LoggerWriter:
    def __init__(self, _logger, level):
        self.logger = _logger
        self.level = level

    def write(self, message):
        if message != '\n':
            self.logger.log(self.level, message)

    def flush(self):
        pass


if sys_utils.isWin() and 'BOATSWAIN_DEBUG' not in os.environ:
    # For windows, all logs must not be printed into stdout/stderr when building .exe release
    sys.stdout = LoggerWriter(logger, logging.INFO)
    sys.stderr = LoggerWriter(logger, logging.ERROR)
