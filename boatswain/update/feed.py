import functools
import tempfile
from typing import List

from PyQt5.QtCore import QObject, pyqtSignal, QTemporaryFile, QUrl, QJsonDocument
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest

from boatswain.common.utils import utils
from boatswain.update import release
from boatswain.update.release import Release


class Feed(QObject):
    url: QUrl = None
    all_releases: List[Release] = []
    network_access: QNetworkAccessManager = QNetworkAccessManager()
    last_release: Release = None
    feed_reply: QNetworkReply = None
    download_reply: QNetworkReply = None
    download_file: QTemporaryFile = None
    n_redirects: int = 0
    __feed_ready: bool = False
    ready = pyqtSignal()
    load_error = pyqtSignal(str)
    download_finished = pyqtSignal()
    download_error = pyqtSignal(str)
    download_progress = pyqtSignal(int, int)

    def __init__(self, github_user_repo):
        super().__init__()
        self.__feed_ready = False
        self.url = QUrl('https://api.github.com/repos/%s/releases' % github_user_repo)

    def isReady(self):
        return self.__feed_ready

    def getUpdates(self, min_release: Release) -> List[Release]:
        updates = []
        for rls in self.all_releases:
            if min_release.lessThan(rls):
                updates.append(rls)
        return updates

    def getReleases(self):
        return self.all_releases

    def load(self):
        if self.feed_reply and not self.feed_reply.isFinished():
            return
        request = QNetworkRequest(self.url)
        self.feed_reply = self.network_access.get(request)
        self.feed_reply.finished.connect(self.handleFeedFinished)

    def handleFeedFinished(self):
        if self.feed_reply.error() != QNetworkReply.NoError:
            self.load_error.emit(self.feed_reply.errorString())
            return
        self.all_releases.clear()
        json = self.feed_reply.readAll()
        doc = QJsonDocument.fromJson(json)
        for rls in doc.array():
            self.all_releases.append(Release.fromJson(rls.toObject()))

        self.all_releases.sort(key=functools.cmp_to_key(release.compare_release))
        self.__feed_ready = True
        self.ready.emit()

    def getDownloadFile(self) -> QTemporaryFile:
        return self.download_file

    def downloadRelease(self, rls: Release):
        self.n_redirects = 0
        self.makeDownloadRequest(rls.getDownloadUrl())
        self.last_release = rls

    def makeDownloadRequest(self, url: QUrl):
        if self.download_reply and not self.download_reply.isFinished():
            self.download_reply.disconnect()
            self.download_reply.abort()
            self.download_reply.deleteLater()
        if self.download_file:
            utils.disconnectAllSignals(self.download_file)
            self.download_file.close()
            self.download_file.deleteLater()
            self.download_file = None
        request = QNetworkRequest(url)
        self.download_reply = self.network_access.get(request)
        self.download_reply.downloadProgress.connect(self.handleDownloadProgress)
        self.download_reply.readyRead.connect(self.handleDownloadReadyRead)
        self.download_reply.finished.connect(self.handleDownloadFinished)

    def handleDownloadProgress(self, bytes_received, bytes_total):
        self.download_progress.emit(bytes_received, bytes_total)

    def handleDownloadReadyRead(self):
        if not self.download_file:
            file_name = QUrl(self.last_release.download_url).fileName()
            self.download_file = QTemporaryFile(tempfile.gettempdir() + '/XXXXXX' + file_name, self)
            self.download_file.open()
        self.download_file.write(self.download_reply.readAll())

    def handleDownloadFinished(self):
        if self.download_reply.error() != QNetworkReply.NoError:
            self.download_error.emit(self.download_reply.errorString())
            return
        elif self.download_reply.attribute(QNetworkRequest.RedirectionTargetAttribute):
            if self.n_redirects >= 10:
                self.download_error.emit(self.tr("Too many redirects."))
            redirection_target = self.download_reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
            redirected_url = self.download_reply.url().resolved(redirection_target)
            self.n_redirects += 1
            self.makeDownloadRequest(redirected_url)
            return
        elif not self.download_file:
            self.download_error.emit(self.tr("No data received from server"))
            return
        self.download_finished.emit()
