from app.search import docker_service
from app.search.search_images import AbstractSearchImages


class DockerHubSearcher(AbstractSearchImages):

    def isSupported(self, repo_filter):
        return True

    def searchImages(self, keyword):
        return docker_service.searchDockerhubContainers(keyword)
