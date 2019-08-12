import os
import sys


def locationIsWritable(path):
    if os.path.isdir(path):
        return isDirWritable(path)
    if os.path.isfile(path):
        return isFileWritable(path)
    return False


def isFileWritable(file):
    return isDirWritable(os.path.dirname(file))


def isDirWritable(directory):
    if not sys.platform.startswith('win'):
        return os.access(directory, os.W_OK)

    try:
        filename = os.path.join(directory, "tmp_file_tester.tmp")
        with open(filename, "w") as f:
            f.write('')
        os.remove(filename)
        return True
    except IOError as e:
        # print "{}".format(e)
        return False
