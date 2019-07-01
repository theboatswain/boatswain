from typing import List

from common.models.tag import Tag


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
