from PyQt5.QtCore import QThread

from common.services import docker_service, data_transporter_service


def generate_key(eventType, action):
    return "DAEMON_" + eventType + "_" + action


def listen(eventType, action, func):
    data_transporter_service.listen(generate_key(eventType, action), func)


class BoatswainDaemon(QThread):
    events = docker_service.streamEvents()

    def run(self):
        for event in self.events:
            channel = generate_key(event['Type'], event['Action'])
            data_transporter_service.fire(channel, event)
            # print(event)
