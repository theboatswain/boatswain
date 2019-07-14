from peewee import *

from common.models.base import BaseModel
from common.models.container import Container


class PortMapping(BaseModel):
    """ Model base for port mapping info """

    id = IntegerField(primary_key=True)
    # target container Id
    container = ForeignKeyField(Container, backref='ports')

    # Description about this port
    description = CharField(default='')

    # container port
    port = IntegerField()
    # protocol is either tcp, udp, or sctp.
    protocol = CharField(default='tcp')
    # host port
    targetPort = IntegerField()
