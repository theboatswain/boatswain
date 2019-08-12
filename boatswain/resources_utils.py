import os
from boatswain.common.utils.logging import logger

current_dir = os.path.dirname(__file__)


def get_resource(file):
    path = os.path.join(current_dir, file)
    logger.info("Resolved %s -> %s" % (file, path))
    return path
