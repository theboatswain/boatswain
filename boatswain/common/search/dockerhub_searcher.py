#  This file is part of Boatswain.
#
#      Boatswain is free software: you can redistribute it and/or modify
#      it under the terms of the GNU General Public License as published by
#      the Free Software Foundation, either version 3 of the License, or
#      (at your option) any later version.
#
#      Boatswain is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU General Public License for more details.
#
#      You should have received a copy of the GNU General Public License
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

from typing import List

import requests

from boatswain.common.models.tag import Tag
from boatswain.common.services import docker_service
from boatswain.common.search.search_images import SearchProvider

DOCKERHUB_API = 'https://registry.hub.docker.com/v2'


class DockerHubSearcher(SearchProvider):

    def search(self, keyword, repo):
        items = docker_service.searchDockerhubContainers(keyword)
        for item in items:
            item['from'] = 'dockerhub'
        return items

    def searchTags(self, image_name: str, repo: str) -> List[Tag]:
        tags = self.recursiveFindImageTag(image_name, 100, 1)
        result = []
        for item in tags:
            result.append(Tag(name=item['name'], size=item['full_size']))
        return result

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
