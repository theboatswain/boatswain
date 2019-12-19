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
import tempfile

from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication

from boatswain_updater.utils import sys_utils

ref_dpi = 110
ref_height = 1440
ref_width = 2560


def getRefHeight():
    return rt(800)


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
        tmp = tempfile.NamedTemporaryFile(suffix='.command', mode='w', delete=False)
        tmp.write('#!/bin/sh\n%s\n' % command)
        os.system('chmod u+x ' + tmp.name)
        proc = QProcess()
        proc.start("open", {tmp.name})
        proc.waitForFinished(-1)
    elif sys_utils.isWin():
        os.system("start cmd /c %s" % command)


def rt(pixel):
    rect = getPrimaryScreen().geometry()
    height = min(rect.width(), rect.height())
    width = max(rect.width(), rect.height())
    ratio = min(height / ref_height, width / ref_width)
    device_pixel_ratio = QApplication.instance().devicePixelRatio()
    return round(pixel * ratio * device_pixel_ratio)


def applyFontRatio(point):
    dpi = getPrimaryScreen().physicalDotsPerInch()
    rect = getPrimaryScreen().geometry()
    height = min(rect.width(), rect.height())
    width = max(rect.width(), rect.height())
    ratio_font = min(height * ref_dpi / (dpi * ref_height), width * ref_dpi / (dpi * ref_width))
    device_pixel_ratio = QApplication.instance().devicePixelRatio()
    return round(point * ratio_font * device_pixel_ratio)


def resetStyle():
    default_font = QApplication.font("QMenu")
    default_font.setPointSize(applyFontRatio(13))
    QApplication.setFont(default_font)
