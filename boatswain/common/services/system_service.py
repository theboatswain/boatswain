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
#      along with Boatswain.  If not, see <https://www.gnu.org/licenses/>.
#
#

import os

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication
from boatswain_updater.utils import sys_utils

from boatswain import resources_utils

ref_dpi = 72 if sys_utils.isMac() else 96


def getRefHeight():
    return rt(900)


def getPrimaryScreen():
    return QGuiApplication.primaryScreen()


def getScreenWidth():
    rect = getPrimaryScreen().geometry()
    return rect.width()


def getScreenHeight():
    rect = getPrimaryScreen().geometry()
    return rect.height()


def startTerminalWithCommand(command):
    if sys_utils.isMac():
        term = resources_utils.getExternalResource('run_with_mac_terminal.sh')
        if os.path.exists("/Applications/iTerm.app"):
            term = resources_utils.getExternalResource('run_with_iterm.sh')
        os.system('chmod u+x ' + term)
        os.system("%s \"%s\" &" % (term, command))
    elif sys_utils.isWin():
        os.system("start cmd /c %s" % command)
    else:
        default_linux_term = 'xterm'
        if os.path.exists('/etc/debian_version'):
            default_linux_term = 'x-terminal-emulator'
        elif os.path.exists('/usr/bin/xfce4-terminal'):
            default_linux_term = 'xfce4-terminal'
        elif os.environ['DESKTOP_SESSION'] == 'gnome':
            default_linux_term = 'gnome-terminal'
        elif os.environ['DESKTOP_SESSION'] == 'kde-plasma':
            default_linux_term = 'konsole'
        elif 'COLORTERM' in os.environ:
            default_linux_term = os.environ['COLORTERM']
        elif 'TERM' in os.environ:
            default_linux_term = os.environ['TERM']
        os.system("%s -e %s &" % (default_linux_term, command))


def rt(pixel):
    scale = getPrimaryScreen().logicalDotsPerInch() / ref_dpi
    return round(pixel * scale)


def applyFontRatio(point):
    if sys_utils.isMac():
        return point
    scale = getPrimaryScreen().physicalDotsPerInch() / ref_dpi
    return round(point * 0.8 * scale)


def resetStyle():
    default_font = QApplication.font("QMenu")
    default_font.setPointSize(applyFontRatio(13))
    QApplication.setFont(default_font)
