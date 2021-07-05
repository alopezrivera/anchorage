import unittest

from anchor_tools.bookmarks import load, export, path


class BookmarkTests(unittest.TestCase):

    def test_path(self):
        return path("windows", "edge beta")

    def test_export(self):
        return export(self.test_path(), "bookmarks/bookmarks.json")

    def test_load_from_browser(self):
        load(self.test_path())

    def test_load_from_file(self):
        return load(self.test_export())
