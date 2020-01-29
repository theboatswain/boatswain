#  This file is part of Boatswain.
#
#      Boatswain<https://github.com/theboatswain> is free software: you can redistribute it and/or modify
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
from PyQt5.QtWidgets import QMessageBox

from boatswain.common.ui.custom_ui import BorderedButton
from boatswain.common.utils.utils import tr


def error(header, body):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText(header)
    msg.setInformativeText(body)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def question(header, body):
    box = QMessageBox()
    box.setIcon(QMessageBox.Question)
    box.setWindowTitle(header)
    box.setText(body)
    ok_button = BorderedButton(box)
    ok_button.setText(tr("Ok"))
    ok_button.setDefault(True)
    cancel_button = BorderedButton(box)
    cancel_button.setText(tr("Cancel"))
    cancel_button.setAutoDefault(False)
    box.addButton(cancel_button, QMessageBox.RejectRole)
    box.addButton(ok_button, QMessageBox.AcceptRole)
    return box.exec_()
