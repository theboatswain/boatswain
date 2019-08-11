import semantic_version as semantic_version
from PyQt5.QtCore import QUrl
import platform


class Release:
    changelog = ""
    download_url = ""
    download_size = 0

    def __init__(self, version: str = '') -> None:
        super().__init__()
        self.version = version

    @staticmethod
    def fromJson(object_json):

        version = object_json['tag_name'].toString()
        release = Release(version)
        release.changelog = object_json['body'].toString()

        assets = object_json["assets"].toArray()

        current_platform = platform.system()
        if current_platform == "Darwin":
            plf = 'macOS'
        elif current_platform == 'Windows':
            plf = 'windows'
        else:
            plf = 'unix'

        for asset in assets:
            download_info = asset.toObject()
            if plf in download_info['name'].toString():
                release.download_url = QUrl(download_info["browser_download_url"].toString())
                release.download_size = download_info["size"].toDouble()
        return release

    def getVersion(self):
        return self.version

    def getChangelog(self):
        return self.changelog

    def lessThan(self, release):
        original = semantic_version.Version(self.version)
        new_version = semantic_version.Version(release.version)
        return original < new_version

    def equals(self, release):
        return self.version == release.version

    def lessOrEquals(self, release):
        return self.lessThan(release) or self.equals(release)

    def getDownloadUrl(self):
        return self.download_url


def compare_release(a: Release, b: Release) -> int:
    if b.lessThan(a):
        return -1
    elif b.equals(a):
        return 0
    else:
        return 1
