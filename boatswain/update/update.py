from typing import List

from PyQt5.QtCore import QSettings, pyqtSignal, QCoreApplication, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QAbstractButton, QApplication, QMessageBox

from boatswain.common.services import system_service
from boatswain.common.utils import utils
from boatswain.update import u_type, core
from boatswain.update.feed import Feed
from boatswain.update.release import Release
from boatswain.update.update_ui import UpdateUi


class Update(QDialog):
    installing = pyqtSignal()
    ready = pyqtSignal()
    latest_release: Release = Release()
    releases: List[Release] = []
    updates: List[Release] = []

    def __init__(self, parent, feed: Feed, update_type: int, settings: QSettings = QSettings()) -> None:
        super().__init__(parent)
        self.ui = UpdateUi(self)
        self.feed = feed
        self.update_type = update_type
        self.settings = settings

        if update_type == u_type.ON_APPLICATION_START:
            self.ready.connect(self.showIfUpdatesAvailable)
        if feed.isReady():
            self.handleFeedReady()
        else:
            self.setupLoadingUi()
            feed.load()
            feed.ready.connect(self.handleFeedReady)

    def showIfUpdatesAvailable(self):
        latest_version = self.latest_release.getVersion()
        skip_release = self.getSettingsValue("skipRelease", "", self.settings) == latest_version
        if not latest_version and skip_release:
            self.show()

    def getSettingsValue(self, key, default_value, settings: QSettings):
        return settings.value("Boatswain/" + key, default_value)

    def setSettingsValue(self, key, value, settings: QSettings):
        settings.setValue("Boatswain/" + key, value)

    def removeSetting(self, key, settings: QSettings):
        settings.remove("Boatswain/" + key)

    def handleFeedReady(self):
        release = Release(QApplication.applicationVersion())
        self.updates = self.feed.getUpdates(release)
        if len(self.updates) > 0:
            self.latest_release = self.updates[0]

        if len(self.updates) == 0:
            self.setupNoUpdatesUi()
            return

        self.setupUpdateUi()
        self.ready.emit()

    def setIcon(self, pixmap: QPixmap):
        self.ui.label_icon.setPixmap(pixmap)
        self.ui.label_icon.setHidden(False)

    def setupNoUpdatesUi(self):
        self.resetUi()
        self.setMinimumSize(QSize(400, 120))
        self.resize(400, 120)
        show_widgets = [self.ui.label_info_no_updates, self.ui.button_confirm, self.ui.label_headline_no_updates,
                        self.ui.header_container, self.ui.label_icon]
        for widget in show_widgets:
            widget.show()
        self.ui.button_confirm.setFocus()
        self.ui.label_headline_no_updates.setText(self.replaceAppVars(self.ui.label_headline_no_updates.text()))
        self.ui.button_confirm.clicked.connect(self.accept)
        self.adjustSize()

    def startDownload(self):
        self.feed.downloadRelease(self.latest_release)
        self.disableButtons(True)

    def setupUpdateUi(self):
        self.resetUi()
        self.ui.label_icon.show()
        height = system_service.screen_height / 2.6
        width = height * 2
        self.setMinimumSize(QSize(width, height))
        self.resize(width, height)
        show_widgets = [self.ui.header_container, self.ui.label_changelog, self.ui.button_skip,
                        self.ui.button_cancel, self.ui.button_install, self.ui.label_info, self.ui.release_notes,
                        self.ui.label_headline]
        for widget in show_widgets:
            widget.show()
        labels = [self.ui.label_headline, self.ui.label_info]
        for label in labels:
            label.setText(self.replaceAppVars(label.text()))
        self.ui.label_changelog.setHtml(self.generateChangelogDocument())
        self.ui.label_changelog.setOpenExternalLinks(True)
        self.ui.label_changelog.setReadOnly(True)

        self.feed.download_finished.connect(self.handleDownloadFinished)
        self.feed.download_error.connect(self.handleDownloadError)
        self.feed.download_progress.connect(self.updateProgressBar)
        self.ui.button_confirm.clicked.connect(self.accept)
        self.ui.button_skip.clicked.connect(self.skipRelease)
        self.ui.button_cancel.clicked.connect(self.reject)

        self.ui.button_install.setFocus()
        self.ui.button_install.clicked.connect(self.onButtonInstall)
        self.adjustSize()

    def onButtonInstall(self):
        self.setupDownloadingUi()
        self.startDownload()

    def skipRelease(self):
        self.setSettingsValue('skipRelease', self.latest_release.getVersion(), self.settings)
        self.reject()

    def handleDownloadFinished(self):
        self.setupInstallUi()

    def handleDownloadError(self, message):
        message_box = QMessageBox(self)
        message_box.setIcon(QMessageBox.Warning)
        message_box.setText(self.tr("There was an error while downloading the update."))
        message_box.setInformativeText(message)
        message_box.show()
        self.reject()

    def disableButtons(self, disable: bool):
        buttons = [self.ui.button_cancel, self.ui.button_confirm, self.ui.button_install, self.ui.button_skip]

        for button in buttons:
            button.setDisabled(disable)

    def generateChangelogDocument(self):
        changelog = ''
        changelog_releases = self.updates

        for index, release in enumerate(changelog_releases):
            h2_style = 'font-size: medium;'
            if index > 0:
                h2_style += 'margin-top: 1em;'
            changelog += '<h2 style="' + h2_style + '">' + release.getVersion() + '</h2>'
            changelog += '<p>' + release.getChangelog() + '</p>'
        return changelog

    def setupLoadingUi(self):
        self.resetUi()
        self.setMinimumSize(QSize(500, 120))
        self.resize(500, 120)
        self.ui.header_container.show()
        self.ui.label_headline_loading.show()
        self.ui.progress_bar.show()
        self.ui.progress_bar.setMaximum(0)
        self.ui.progress_bar.setMinimum(0)
        self.ui.label_icon.show()
        self.adjustSize()

    def setupDownloadingUi(self):
        self.resetUi()
        self.setWindowTitle(self.tr("Updating") + " %s…" % QApplication.applicationName())
        self.setMinimumSize(QSize(500, 120))
        self.resize(500, 120)
        show_widgets = [self.ui.header_container, self.ui.label_icon, self.ui.progress_bar, self.ui.label_downloading,
                        self.ui.button_cancel_loading]
        for widget in show_widgets:
            widget.show()

        self.ui.button_cancel_loading.setEnabled(True)
        self.ui.button_cancel_loading.setFocus()
        self.ui.button_cancel_loading.clicked.connect(self.reject)
        self.adjustSize()

    def setupInstallUi(self):
        self.resetUi()
        self.setWindowTitle(self.tr("Updating") + " %s…" % QApplication.applicationName())
        self.setMinimumSize(QSize(500, 120))
        self.resize(500, 120)
        show_widgets = [self.ui.header_container, self.ui.label_icon, self.ui.progress_bar,
                        self.ui.button_install_and_relaunch, self.ui.label_install_and_relaunch]
        for widget in show_widgets:
            widget.show()

        self.ui.progress_bar.setMaximum(0)
        self.ui.progress_bar.setValue(0)

        self.ui.button_install_and_relaunch.setEnabled(True)
        self.ui.button_install_and_relaunch.setFocus()
        self.ui.button_install_and_relaunch.clicked.connect(self.installUpdate)
        self.adjustSize()

    def installUpdate(self):
        file = self.feed.getDownloadFile()
        core.install_update(file)
        self.installing.emit()
        self.accept()

    def resetUi(self):
        hidden_widgets = [self.ui.header_container, self.ui.label_icon, self.ui.label_headline_loading,
                          self.ui.label_info, self.ui.release_notes, self.ui.button_install_and_relaunch,
                          self.ui.label_headline, self.ui.label_downloading, self.ui.label_install_and_relaunch,
                          self.ui.label_info_no_updates, self.ui.label_headline_no_updates,
                          self.ui.label_changelog, self.ui.progress_bar, self.ui.button_skip,
                          self.ui.button_cancel, self.ui.button_cancel_loading, self.ui.button_confirm,
                          self.ui.button_install]

        for widget in hidden_widgets:
            widget.hide()
            utils.disconnectAllSignals(widget)
        self.ui.progress_bar.reset()
        self.adjustSize()

    def replaceAppVars(self, string):
        new_str = string.replace("%APPNAME%", QCoreApplication.applicationName())
        new_str = new_str.replace("%CURRENT_VERSION%", QCoreApplication.applicationVersion())
        new_str = new_str.replace("%UPDATE_VERSION%", self.latest_release.getVersion())
        return new_str

    def updateProgressBar(self, bytes_received, bytes_total):
        self.ui.progress_bar.show()
        self.ui.progress_bar.setMaximum(bytes_total / 1024)
        self.ui.progress_bar.setValue(bytes_received / 1024)
