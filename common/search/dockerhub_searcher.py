import requests

from common.services import docker_service
from common.search.search_images import AbstractSearchImages

DOCKERHUB_API = 'https://registry.hub.docker.com/v2'


class DockerHubSearcher(AbstractSearchImages):

    def searchImageTags(self, image_name):
        return self.recursiveFindImageTag(image_name, 100, 1)

    def recursiveFindImageTag(self, image_name, page_size, page):
        image_location = image_name
        if '/' not in image_name:
            image_location = 'library/' + image_name
        url = DOCKERHUB_API + "/repositories/%s/tags/?page_size=%d&page=%d" % (image_location, page_size, page)
        response = requests.get(url).json()
        result = response['results']
        if response['next']:
            result += self.recursiveFindImageTag(image_name, page_size, page + 1)
        return result

    def isSupported(self, repo_filter):
        return True

    def searchImages(self, keyword):
        return docker_service.searchDockerhubContainers(keyword)
