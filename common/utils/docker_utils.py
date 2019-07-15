from PyQt5.QtWidgets import QMessageBox

from common.models.container import Container


def notifyDockerNotAvailable():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Docker daemon isn't running")
    msg.setInformativeText("Boatswain requires to have Docker daemon already up and running")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def notifyContainerNotRunning(container: Container, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Container %s is not running" % container.name)
    msg.setInformativeText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
