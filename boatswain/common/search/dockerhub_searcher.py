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
from boatswain.common.search.search_images import SearchProvider

DOCKERHUB_API = 'https://registry.hub.docker.com/v2'
DOCKERHUB_SEARCH_API = 'https://hub.docker.com/api/content/v1/products/search'


class DockerHubSearcher(SearchProvider):

    def search(self, keyword, repo):
        url = "%s/?q=%s&type=image&page=1&page_size=25" % (DOCKERHUB_SEARCH_API, keyword)
        res = requests.get(url, headers={'Search-Version': 'v3'})
        items = []
        if res.ok:
            for item in res.json()['summaries']:
                image = {
                    'from': repo,
                    'name': item['name'],
                    'description': item['short_description'],
                    'star_count': item['star_count']
                }
                if 'logo_url' in item and type(item['logo_url']) is dict:
                    for key in list(item['logo_url']):
                        if len(item['logo_url'][key]) > 0:
                            image['logo_url'] = item['logo_url'][key]
                if 'logo_url' not in image:
                    image['logo_url'] = None
                image['is_official'] = item['filter_type'] == 'official'
                items.append(image)
        return items

    def searchTags(self, image_name: str, repo: str) -> List[Tag]:
        tags = self.recursiveFindImageTag(image_name, 100, 1)
        result = []
        for item in tags:
            if item['full_size'] is None:
                continue
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
