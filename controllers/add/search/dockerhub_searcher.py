from controllers.add.search.search_images import AbstractSearchImages
from services import docker_service


class DockerHubSearcher(AbstractSearchImages):

    def isSupported(self, repo_filter):
        return True

    def search_images(self, keyword):
        return docker_service.search_dockerhub_containers(keyword)
