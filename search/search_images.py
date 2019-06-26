class SearchProvider:

    def search(self, keyword, repo_filter):
        raise NotImplementedError("Should have implemented this")


class DefaultSearchImages(SearchProvider):

    def search(self, keyword, repo_filter):
        return []


class AbstractSearchImages(SearchProvider):

    def __init__(self, search_provider: SearchProvider) -> None:
        super().__init__()
        self.__search_provider = search_provider

    def search(self, keyword, repo_filter):
        images = self.__search_provider.search(keyword, repo_filter)
        if self.isSupported(repo_filter):
            images += self.search_images(keyword)
        return images

    def isSupported(self, repo_filter):
        raise NotImplementedError("Should have implemented this")

    def search_images(self, keyword):
        raise NotImplementedError("Should have implemented this")
