from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize

from boatswain.common.utils.custom_ui import BQSizePolicy


class UpdateUi:
    def __init__(self, dialog) -> None:
        dialog.setMinimumSize(QSize(400, 120))
        dialog.setModal(True)
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(dialog)
        self.vertical_layout_2.setContentsMargins(20, 11, 11, 11)
        self.vertical_layout_2.setSpacing(0)
        self.header_container = QtWidgets.QWidget(dialog)
        self.grid_layout = QtWidgets.QGridLayout(self.header_container)
        self.grid_layout.setContentsMargins(0, 6, 0, 0)
        self.grid_layout.setHorizontalSpacing(24)
        self.grid_layout.setVerticalSpacing(6)
        self.label_headline = QtWidgets.QLabel(self.header_container)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(105)
        self.label_headline.setFont(font)
        self.grid_layout.addWidget(self.label_headline, 0, 2, 1, 1)

        self.label_headline_loading = QtWidgets.QLabel(self.header_container)
        self.grid_layout.addWidget(self.label_headline_loading, 0, 2, 1, 1)

        self.label_downloading = QtWidgets.QLabel(self.header_container)
        self.label_downloading.setFont(font)
        self.grid_layout.addWidget(self.label_downloading, 0, 2, 1, 1)

        self.label_install_and_relaunch = QtWidgets.QLabel(self.header_container)
        self.label_install_and_relaunch.setFont(font)
        self.grid_layout.addWidget(self.label_install_and_relaunch, 0, 2, 1, 1)

        self.progress_bar = QtWidgets.QProgressBar(self.header_container)
        self.grid_layout.addWidget(self.progress_bar, 1, 2, 2, 1)

        self.label_headline_no_updates = QtWidgets.QLabel(self.header_container)
        self.grid_layout.addWidget(self.label_headline_no_updates, 0, 2, 1, 1)

        self.label_info_no_updates = QtWidgets.QLabel(self.header_container)
        self.grid_layout.addWidget(self.label_info_no_updates, 1, 2, 2, 1)

        self.label_icon = QtWidgets.QLabel(self.header_container)
        self.label_icon.setSizePolicy(BQSizePolicy(width=QtWidgets.QSizePolicy.Minimum))
        self.grid_layout.addWidget(self.label_icon, 0, 0, 3, 1)
        self.label_info = QtWidgets.QLabel(self.header_container)
        self.label_info.setSizePolicy(BQSizePolicy(width=QtWidgets.QSizePolicy.Expanding))
        self.label_info.setWordWrap(True)
        self.grid_layout.addWidget(self.label_info, 1, 2, 2, 1)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.release_notes = QtWidgets.QLabel(self.header_container)
        self.release_notes.setFont(font)
        self.release_notes.setSizePolicy(BQSizePolicy(width=QtWidgets.QSizePolicy.Expanding))
        self.grid_layout.addWidget(self.release_notes, 2, 2, 1, 1)
        self.vertical_layout_2.addWidget(self.header_container)
        self.label_changelog = QtWidgets.QTextBrowser(self.header_container)
        self.label_changelog.setSizePolicy(BQSizePolicy(height=QtWidgets.QSizePolicy.Expanding))
        self.grid_layout.addWidget(self.label_changelog, 3, 2, 1, 1)

        self.button_container = QtWidgets.QWidget(dialog)
        self.button_container.setSizePolicy(BQSizePolicy(height=QtWidgets.QSizePolicy.Minimum))
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.button_container)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(12)
        self.button_skip = QtWidgets.QPushButton(self.button_container)
        self.horizontal_layout.addWidget(self.button_skip)
        spacer_item1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontal_layout.addItem(spacer_item1)
        self.button_cancel = QtWidgets.QPushButton(self.button_container)
        self.horizontal_layout.addWidget(self.button_cancel)
        self.button_install = QtWidgets.QPushButton(self.button_container)
        self.horizontal_layout.addWidget(self.button_install)
        self.button_install_and_relaunch = QtWidgets.QPushButton(self.button_container)
        self.horizontal_layout.addWidget(self.button_install_and_relaunch)
        self.button_confirm = QtWidgets.QPushButton(self.button_container)
        self.horizontal_layout.addWidget(self.button_confirm)
        self.button_cancel_loading = QtWidgets.QPushButton(self.button_container)
        self.horizontal_layout.addWidget(self.button_cancel_loading)
        self.grid_layout.addWidget(self.button_container, 4, 2, 1, 1)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label_headline_loading.setText(_translate("UpdateDialog", "Loading update information…"))
        self.label_headline.setText(_translate("UpdateDialog", "A new version of %APPNAME% is available!"))
        self.label_info.setText(_translate("UpdateDialog", "%APPNAME% %UPDATE_VERSION% is now available "
                                                           "-- you have %CURRENT_VERSION%. "
                                                           "Would you like to update now?\n"))
        self.release_notes.setText(_translate("UpdateDialog", "Release Notes:"))
        self.label_info_no_updates.setText(_translate("UpdateDialog", "There are currently no updates available."))
        self.label_downloading.setText(_translate("UpdateDialog", "Downloading update…"))
        self.label_headline_no_updates.setText(_translate("UpdateDialog", "You are using %APPNAME% %CURRENT_VERSION%."))
        self.button_cancel_loading.setText(_translate("UpdateDialog", "Cancel"))
        self.button_install.setText(_translate("UpdateDialog", "Install Update"))
        self.button_install_and_relaunch.setText(_translate("UpdateDialog", "Install and Relaunch"))
        self.label_install_and_relaunch.setText(_translate("UpdateDialog", "Ready to Install"))
        self.button_confirm.setText(_translate("UpdateDialog", "OK"))
        self.button_cancel.setText(_translate("UpdateDialog", "Remind Me Later"))
        self.button_skip.setText(_translate("UpdateDialog", "Skip This Version"))
