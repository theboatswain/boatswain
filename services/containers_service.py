from domains.container import Container
from services import data_transporter_service
from utils.constants import CONTAINER_CHANNEL


def install_container(image_name, description):
    container = Container(name=image_name, description=description, tag='latest', status=0)
    container.save()
    data_transporter_service.fire(CONTAINER_CHANNEL, container)
