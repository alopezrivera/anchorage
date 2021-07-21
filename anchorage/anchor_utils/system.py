import os
import platform


def operating_system():
    return platform.system().lower()


def home():
    return os.environ['HOME']
