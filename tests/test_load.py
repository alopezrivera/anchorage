import unittest

from src.bookmarks import load, export, path


class Tests(unittest.TestCase):

    def test_path(self):
        return path("windows", "edge beta")

    def test_export(self):
        return export(self.test_path(), "data/bookmarks.json")

    def test_loadfile(self):
        return load(self.test_export())
