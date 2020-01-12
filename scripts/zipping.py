import os
import sys
import zipfile
from os.path import basename


def isMac():
    return sys.platform.startswith('darwin')


def isWin():
    return sys.platform.startswith('win')


def isLinux():
    return sys.platform.startswith('linux')


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


folder = sys.argv[1]
architect = sys.argv[2]
version = sys.argv[3]
if isWin():
    file_name = "Boatswain-win-%s-portable-%s.zip" % (architect, version)
elif isMac():
    file_name = "Boatswain-macOS-%s.zip" % version
else:
    file_name = "Boatswain-linux-%s-%s.zip" % (architect, version)

zipf = zipfile.ZipFile(os.path.join(os.path.dirname(folder), file_name), 'w', zipfile.ZIP_DEFLATED)
zipdir(folder, zipf)
zipf.close()
