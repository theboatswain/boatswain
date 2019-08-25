from PyQt5.QtWidgets import QMessageBox


def error(header, body):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText(header)
    msg.setInformativeText(body)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
