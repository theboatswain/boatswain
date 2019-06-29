from common.models.container import Container
from common.services import data_transporter_service
from common.utils.constants import CONTAINER_CHANNEL


def installContainer(image_name, description):
    container = Container(name=image_name, description=description, tag='latest', status=0)
    container.save()
    data_transporter_service.fire(CONTAINER_CHANNEL, container)
