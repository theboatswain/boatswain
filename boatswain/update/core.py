from PyQt5.QtCore import QTemporaryFile


def install_update(zip_file: QTemporaryFile):

    # Todo: implement install logic
    zip_file.close()
    zip_file.deleteLater()
