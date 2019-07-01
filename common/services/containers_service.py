from common.models.container import Container
from common.search.dockerhub_searcher import DockerHubSearcher
from common.search.search_images import SearchImages

# Initialising search engines
search_engine = SearchImages()
search_engine.addSearchProvider(DockerHubSearcher())


def installContainer(image_name, repo, description):
    container = Container(name=image_name, description=description, tag='latest', status=0)
    container.save()
    tags = search_engine.searchTags(image_name, repo)
    for tag in tags:
        tag.container = container
        tag.save()
    return container


def isAppInstalled(image_name):
    # Todo: Should we do this? [Performance]
    for container in Container.select():
        if container.name == image_name:
            return True
    return False


def search_images(keyword, repo_filter):
    return search_engine.search(keyword, repo_filter)
