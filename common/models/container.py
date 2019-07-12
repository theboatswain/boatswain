from peewee import *

from common.models.base import BaseModel


class Container(BaseModel):
    """ Model object represents for a docker container"""

    id = IntegerField(primary_key=True)
    # container short hash Id, ex: 8932a3a78c7f
    container_id = CharField(default='')
    # docker container name
    # image name, ex: mongo
    image_name = CharField()
    # image tag, ex: 1.0
    tag = CharField()
    # a short info that describes about app/soft/tool...
    description = TextField()
    # avatar for the container
    avatar = CharField(default='')
    # docker registry, default is docker hub, users can also use a custom registry
    repo = CharField(default='dockerhub')
