import os
import platform


def startTerminalWithCommand(command):
    current_platform = platform.system()
    if current_platform == "Darwin":
        os.system("osascript -e 'tell app \"Terminal\" to do script \"%s\"'" % command)
