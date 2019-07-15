import os
import platform
import tempfile

from PyQt5.QtCore import QProcess


def startTerminalWithCommand(command):
    current_platform = platform.system()
    if current_platform == "Darwin":
        tmp = tempfile.NamedTemporaryFile(suffix='.command', mode='w', delete=False)
        tmp.write('#!/bin/sh\n%s\n' % command)
        os.system('chmod u+x ' + tmp.name)
        proc = QProcess()
        proc.start("open", {tmp.name})
        proc.waitForFinished(-1)
