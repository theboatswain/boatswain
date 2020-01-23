from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialogButtonBox

from boatswain.common.services.system_service import rt, applyFontRatio
from boatswain.common.ui.custom_ui import BQSizePolicy, BorderedButton
from boatswain.common.utils.utils import tr


class ConnectionManagementUi(object):

    def __init__(self, dialog) -> None:
        super().__init__()
        dialog.resize(rt(731), rt(200))
        self.verticalLayout = QtWidgets.QVBoxLayout(dialog)
        self.label = QtWidgets.QLabel(dialog)
        self.label.setSizePolicy(BQSizePolicy(v_stretch=2))
        font = QtGui.QFont()
        font.setPointSize(applyFontRatio(18))
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)
        self.message = QtWidgets.QLabel(dialog)
        self.message.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.message)
        self.widget = QtWidgets.QWidget(dialog)
        self.widget.setSizePolicy(BQSizePolicy(v_stretch=3))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(rt(6))
        self.protocol = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(applyFontRatio(13))
        font.setBold(True)
        font.setWeight(75)
        self.protocol.setFont(font)
        self.horizontalLayout.addWidget(self.protocol)
        self.url = QtWidgets.QLineEdit(self.widget)
        self.url.setProperty('class', 'border-button')
        self.horizontalLayout.addWidget(self.url)
        self.verticalLayout.addWidget(self.widget)
        self.button_box = QtWidgets.QDialogButtonBox(dialog)
        self.button_box.setOrientation(QtCore.Qt.Horizontal)
        self.ok_button = BorderedButton(dialog)
        self.ok_button.setDefault(True)
        self.cancel_button = BorderedButton(dialog)
        self.cancel_button.setAutoDefault(False)
        self.button_box.addButton(self.cancel_button, QDialogButtonBox.RejectRole)
        self.button_box.addButton(self.ok_button, QDialogButtonBox.AcceptRole)
        self.verticalLayout.addWidget(self.button_box)

        self.retranslateUi(dialog)
        self.button_box.rejected.connect(dialog.reject)

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(tr("Connection Management Dialog"))
        self.label.setText(tr("Docker connection configuration"))
        self.protocol.setText(tr("Docker URI:"))
        self.cancel_button.setText(tr("Cancel"))
        self.ok_button.setText(tr("Test connection..."))
