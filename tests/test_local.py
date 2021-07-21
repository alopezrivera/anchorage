import os
import shutil
import unittest

from anchorage import anchor_locally, load, path, add_local as add, server
from anchorage.anchor_tools.local import setup, init


class Tests(unittest.TestCase):

    def test_all(self):
        t_setup()
        t_init()
        t_add()
        t_server()


test_archive = r"C:\Users\xXY4n\Projects\Anchorage\tests\test_archive"


def t_setup():
    print("LOCAL ARCHIVE TESTS: SETUP")
    if os.path.isdir(test_archive):
        shutil.rmtree(test_archive)
    setup(archive=test_archive)


def t_init():
    print("LOCAL ARCHIVE TESTS: INITIALIZATION")
    init(archive=test_archive)


def t_add():
    print("LOCAL ARCHIVE TESTS: ADDITION")
    add(url="http://larsblackmore.com/AcikmeseBlackmoreAutomatica10.pdf",
        archive=test_archive)


def t_server():
    print("LOCAL ARCHIVE TESTS: SERVER")
    server(archive=test_archive, instakill=True)
