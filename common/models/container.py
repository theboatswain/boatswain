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

    # customisable name
    name = CharField(default='')
    # image tag, ex: 1.0
    tag = CharField()
    # a short info that describes about app/soft/tool...
    description = TextField()
    # avatar for the container
    avatar = CharField(default='')
    # docker registry, default is docker hub, users can also use a custom registry
    repo = CharField(default='dockerhub')
    # limit amount of memory for this container
    memory_limit = IntegerField(default=0)
    # unit of the memory limit MB/GB
    memory_limit_unit = CharField(default='MB')
    # limit number of cpus for this container
    cpu_limit = FloatField(default=0.0)
    # unit of the cpu limit CPUs/Period/Quota
    cpu_limit_unit = CharField(default='CPUs')
