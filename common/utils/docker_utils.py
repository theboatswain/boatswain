from PyQt5.QtWidgets import QMessageBox


def notify_docker_not_available():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Docker daemon isn't running")
    msg.setInformativeText("Boatswain requires to have Docker daemon already up and running")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()