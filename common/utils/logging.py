import logging
import os


from common.utils.constants import APP_LOG_DIR

log_file = os.path.join(APP_LOG_DIR, 'boatswain.log')
if not os.path.isdir(APP_LOG_DIR):
    os.makedirs(APP_LOG_DIR)

logging.basicConfig(filename=log_file,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('boatswain')
