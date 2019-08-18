import os

current_dir = os.path.dirname(__file__)


def get_resource(file):
    path = os.path.join(current_dir, file)
    return path
