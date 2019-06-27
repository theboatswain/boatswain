import os

from peewee import *

from utils.constants import APP_DATA_DIR, APP_DB

db = SqliteDatabase(os.path.join(APP_DATA_DIR, APP_DB))


class BaseModel(Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        database = db
