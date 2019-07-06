from peewee import *

from common.models.base import BaseModel


class Container(BaseModel):
    """ Model object represents for a docker container"""

    id = IntegerField(primary_key=True)
    # docker container name
    name = CharField()
    # image name, ex: mongo
    image_name = CharField()
    # image tag, ex: 1.0
    tag = CharField()
    # a short info that describes about app/soft/tool...
    description = TextField()
    # installed/removed
    status = IntegerField()
    avatar = CharField(default='')
    # docker registry, default is docker hub, users can also use a custom registry
    repo = CharField(default='dockerhub')
