import os
import shutil
import unittest

from anchorage import add_local as add, server
from anchor_tools.local import setup, init


test_archive = r"C:\Users\xXY4n\Projects\Anchorage\tests\archive"


class LocalArchiveTests(unittest.TestCase):

    def setup(self):
        if os.path.isdir(test_archive):
            shutil.rmtree(test_archive)
        setup(archive=test_archive)

    def init(self):
        init(archive=test_archive)

    def add(self):
        add(url="http://larsblackmore.com/AcikmeseBlackmoreAutomatica10.pdf",
            archive=test_archive)

    def server(self):
        server(archive=test_archive, instakill=True)

    def test(self):
        self.setup()
        self.init()
        self.add()
        self.server()
