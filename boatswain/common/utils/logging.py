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

from boatswain.common.utils.constants import APP_LOG_DIR

log_file = os.path.join(APP_LOG_DIR, 'boatswain.log')
if not os.path.isdir(APP_LOG_DIR):
    os.makedirs(APP_LOG_DIR)

logging.basicConfig(filename=log_file,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logging.getLogger('boatswain')

logger = logging.getLogger('boatswain')


class LoggerWriter:
    def __init__(self, _logger, level):
        self.logger = _logger
        self.level = level

    def write(self, message):
        if message != '\n':
            self.logger.log(self.level, message)

    def flush(self):
        pass


sys.stdout = LoggerWriter(logger, logging.INFO)
sys.stderr = LoggerWriter(logger, logging.ERROR)
