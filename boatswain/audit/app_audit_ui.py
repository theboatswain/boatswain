from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QScrollArea, QFrame, QWidget, QSizePolicy, QVBoxLayout

from boatswain.common.models.container import Container
from boatswain.common.services.system_service import rt
from boatswain.common.ui.custom_ui import BQSizePolicy


class AppAuditUi(object):

    def __init__(self, dialog: QDialog, container: Container, handler) -> None:
        self.container = container
        self.handler = handler
        self.dialog = dialog
        width = 680
        dialog.setFixedWidth(width)
        dialog.setSizePolicy(BQSizePolicy(h_stretch=1))
        dialog.setMinimumWidth(width)
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.label = QtWidgets.QLabel(dialog)
        self.label.setWordWrap(True)
        self.verticalLayout.addWidget(self.label)

        self.line = QFrame(self.dialog)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        self.scroll_area = QScrollArea(dialog)
        self.scroll_area.setSizePolicy(BQSizePolicy(v_stretch=2))
        self.scroll_area.setFrameShape(QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QFrame.Plain)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setMaximumHeight(200)

        self.app_list = QWidget(dialog)
        self.app_list.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.app_list_layout = QVBoxLayout(self.app_list)
        self.app_list_layout.setSpacing(0)
        self.app_list_layout.setAlignment(Qt.AlignTop)
        self.app_list_layout.setContentsMargins(0, rt(1), 0, 0)
        self.app_list.setLayout(self.app_list_layout)
        self.scroll_area.setWidget(self.app_list)

        self.verticalLayout.addWidget(self.scroll_area)

        self.line = QFrame(self.dialog)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.verticalLayout.addWidget(self.line)

        self.toolbox = QtWidgets.QWidget(dialog)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.toolbox)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.cancel = QtWidgets.QPushButton(self.toolbox)
        self.horizontalLayout.addWidget(self.cancel)
        self.hidden = QtWidgets.QWidget(self.toolbox)
        self.hidden.setSizePolicy(BQSizePolicy(h_stretch=1))
        self.horizontalLayout.addWidget(self.hidden)
        self.old_conf = QtWidgets.QPushButton(self.toolbox)
        self.horizontalLayout.addWidget(self.old_conf)
        self.merge = QtWidgets.QPushButton(self.toolbox)
        self.horizontalLayout.addWidget(self.merge)
        self.verticalLayout.addWidget(self.toolbox)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "There are some changed configurations that required the container "
                                                    "to be reset. Please consider using Volume Mapping to preserve "
                                                    "your data."))
        self.cancel.setText(_translate("MainWindow", "Cancel"))
        self.old_conf.setToolTip(_translate("MainWindow", "Launch the application with the old configurations"))
        self.old_conf.setText(_translate("MainWindow", "Use the old configuations"))
        self.merge.setToolTip(_translate("MainWindow", "Merge the old with the new configurations and "
                                                       "launch the application"))
        self.merge.setText(_translate("MainWindow", "Merge"))
