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

from PyQt5.QtCore import QThread

from boatswain.common.services import data_transporter_service, docker_service
from boatswain.common.utils.logging import logger


def generate_key(event_type, action):
    return "DAEMON_" + event_type + "_" + action


def listen(event_type, action, func):
    data_transporter_service.listen(generate_key(event_type, action), func)


def deregister(event_type, action, func):
    key = generate_key(event_type, action)
    data_transporter_service.deregister(key, func)


class BoatswainDaemon(QThread):
    def run(self):
        self.events = docker_service.streamEvents()
        for event in self.events:
            channel = generate_key(event['Type'], event['Action'])
            try:
                data_transporter_service.fire(channel, event)
            except Exception as e:
                logger.error("exception occurred", e, exc_info=1)
            logger.debug("Received an event: %s", event)
