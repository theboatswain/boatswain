from app.search import docker_service
from app.search.search_images import AbstractSearchImages


class DockerHubSearcher(AbstractSearchImages):

    def isSupported(self, repo_filter):
        return True

    def search_images(self, keyword):
        return docker_service.search_dockerhub_containers(keyword)
