import os


def readFile(file_path):
    if os.path.isfile(file_path):
        with open(file_path) as f:
            return f.read()
    raise FileNotFoundError(file_path)
