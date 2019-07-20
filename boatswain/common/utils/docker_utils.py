#  This file is part of Boatswain.
#
#      Boatswain is free software: you can redistribute it and/or modify
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
#      along with Foobar.  If not, see <https://www.gnu.org/licenses/>.
#
#

from PyQt5.QtWidgets import QMessageBox

from boatswain.common.models.container import Container


def notifyDockerNotAvailable():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Docker daemon isn't running")
    msg.setInformativeText("Boatswain requires to have Docker daemon already up and running")
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def notifyDockerException(message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Exception occurred!!!")
    msg.setInformativeText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def notifyContainerNotRunning(container: Container, message):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)

    msg.setText("Container %s is not running" % container.name)
    msg.setInformativeText(message)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()
