import os

from peewee import *

from common.utils.constants import APP_DATA_DIR, APP_DB

db = SqliteDatabase(os.path.join(APP_DATA_DIR, APP_DB))


class BaseModel(Model):
    """ Base model for boat swain """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        database = db
