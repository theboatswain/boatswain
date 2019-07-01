class SearchProvider:

    def search(self, keyword, repo_filter):
        raise NotImplementedError("Should have implemented this")

    def searchTags(self, image_name, repo):
        raise NotImplementedError("Should have implemented this")


class DefaultSearchImages(SearchProvider):

    def searchTags(self, image_name, repo):
        return []

    def search(self, keyword, repo_filter):
        return []


class AbstractSearchImages(SearchProvider):

    def searchTags(self, image_name, repo):
        tags = self.__search_provider.searchTags(image_name, repo)
        if self.isSupported(repo):
            tags += self.searchImageTags(image_name)
        return tags

    def __init__(self, search_provider: SearchProvider) -> None:
        super().__init__()
        self.__search_provider = search_provider

    def search(self, keyword, repo_filter):
        images = self.__search_provider.search(keyword, repo_filter)
        if self.isSupported(repo_filter):
            images += self.searchImages(keyword)
        return images

    def isSupported(self, repo_filter):
        raise NotImplementedError("Should have implemented this")

    def searchImages(self, keyword):
        raise NotImplementedError("Should have implemented this")

    def searchImageTags(self, image_name):
        raise NotImplementedError("Should have implemented this")