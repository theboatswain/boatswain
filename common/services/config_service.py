from peewee import DoesNotExist

from common.models.configurations import Configuration
from common.models.container import Container


def getAppConf(container: Container, key: str) -> Configuration:
    return Configuration.get(Configuration.container == container, Configuration.name == key)


def isAppConf(container: Container, key: str, value: str) -> bool:
    try:
        conf = getAppConf(container, key)
        return conf.value == value
    except DoesNotExist:
        return False


def setAppConf(container: Container, key: str, value: str):
    try:
        conf = getAppConf(container, key)
        conf.value = value
        conf.save()
    except DoesNotExist:
        Configuration.create(container=container, name=key, value=value)
