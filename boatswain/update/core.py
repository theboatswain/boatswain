import os
import tempfile
import zipfile

from PyQt5.QtCore import QTemporaryFile
from boatswain.common.utils.logging import logger


def install_update(update_file: QTemporaryFile):
    extract_to = tempfile.mkdtemp(suffix='', prefix='boatswain_x_zip_', dir=None)
    zip_file = zipfile.ZipFile(update_file.fileName(), 'r')
    for file in zip_file.infolist():
        zip_file.extract(file, extract_to)
        os.chmod(os.path.join(extract_to, file.filename), 0o755)  # make executable
    zip_file.close()
    logger.info("Extracted update file into %s" % extract_to)
    update_file.close()
    update_file.deleteLater()

