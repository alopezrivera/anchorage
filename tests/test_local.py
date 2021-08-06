import os
import shutil
import unittest

from anchorage.anchor_tools.local import setup, init, add, server


class Tests(unittest.TestCase):

    def test_all(self):
        t_setup()
        t_init()
        t_add()
        t_server()


test_archive = r"C:\Users\xXY4n\Projects\Anchorage\tests\test_archive"


def t_setup():
    print("\nLOCAL ARCHIVE TESTS: SETUP\n")
    if os.path.isdir(test_archive):
        shutil.rmtree(test_archive)
    setup(archive=test_archive)


def t_init():
    print("\nLOCAL ARCHIVE TESTS: INITIALIZATION\n")
    init(archive=test_archive)


def t_add():
    print("\nLOCAL ARCHIVE TESTS: ADDITION\n")
    add(url="http://larsblackmore.com/AcikmeseBlackmoreAutomatica10.pdf",
        archive=test_archive)


def t_server():
    print("\nLOCAL ARCHIVE TESTS: SERVER\n")
    server(archive=test_archive, instakill=True)
