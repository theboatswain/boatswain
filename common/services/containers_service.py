from common.models.container import Container
from common.search.dockerhub_searcher import DockerHubSearcher
from common.search.search_images import SearchImages

# Initialising search engines
search_engine = SearchImages()
search_engine.addSearchProvider(DockerHubSearcher())


def install_container(image_name, repo='dockerhub', description='', tag='latest', environments=None, ports=None):
    container = Container(image_name=image_name, description=description, tag=tag, status='INSTALLED')
    container.save()

    if environments is not None:
        for env in environments:
            env.container = container
            env.save()
    if ports is not None:
        for port in ports:
            port.container = container;
            port.save()

    tags = search_engine.searchTags(image_name, repo)
    for tag in tags:
        tag.container = container
        tag.save()
    return container


def is_app_installed(image_name):
    # Todo: Should we do this? [Performance]
    # Yes, we should, let's do it by checking image name and registry url
    for container in Container.select():
        if container.image_name == image_name:
            return True
    return False


def search_images(keyword, repo_filter):
    return search_engine.search(keyword, repo_filter)
