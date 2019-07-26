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

from boatswain.common.models.tag import Tag


class SearchProvider:

    def search(self, keyword, repo):
        raise NotImplementedError("Should have implemented this")

    def searchTags(self, image_name: str, repo: str) -> List[Tag]:
        raise NotImplementedError("Should have implemented this")

    def isSupported(self, repo):
        raise NotImplementedError("Should have implemented this")


class SearchImages(SearchProvider):

    providers: List[SearchProvider] = []

    def isSupported(self, repo):
        return True

    def addSearchProvider(self, provider: SearchProvider):
        self.providers.append(provider)

    def search(self, keyword, repo):
        result = []
        for provider in self.providers:
            if provider.isSupported(repo):
                result += provider.search(keyword, repo)
        return result

    def searchTags(self, image_name: str, repo: str) -> List[Tag]:
        result = []
        for provider in self.providers:
            if provider.isSupported(repo):
                result += provider.searchTags(image_name, repo)
        return result
