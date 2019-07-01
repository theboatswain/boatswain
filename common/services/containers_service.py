from common.search.dockerhub_searcher import DockerHubSearcher
from common.search.search_images import DefaultSearchImages
from common.models.container import Container
from common.services import data_transporter_service
from common.utils.constants import CONTAINER_CHANNEL

# Initialising search engines
search_engine = DefaultSearchImages()
search_engine = DockerHubSearcher(search_engine)


def installContainer(image_name, description):
    container = Container(name=image_name, description=description, tag='latest', status=0)
    container.save()
    data_transporter_service.fire(CONTAINER_CHANNEL, container)


def search_images(keyword, repo_filter):
    return search_engine.search(keyword, repo_filter)
