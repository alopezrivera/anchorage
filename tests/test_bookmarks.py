import unittest

from anchor_tools.bookmarks import bookmarks, load, export, path


class BookmarkTests(unittest.TestCase):

    def test_path(self):
        return path("windows", "edge beta")

    def test_export(self):
        return export(self.test_path(), "bookmarks/bookmarks.json")

    def test_load_from_browser(self):
        return load(self.test_path())

    def test_load_from_file(self):
        return load(self.test_export())

    def test_tags(self):
        print(bookmarks(self.test_load_from_browser()).bookmarks)

    def test_filters(self):
        print(bookmarks(self.test_load_from_browser(),
                        drop_directories=['Favorites bar', 'Other favorites']).bookmarks)
