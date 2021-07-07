import unittest

from anchor_tools.bookmarks import bookmarks, load, export, path


class BookmarkTests(unittest.TestCase):

    def test_path(self):
        return path("windows", "edge beta")

    def test_export(self):
        return export(self.test_path(), "bookmarks/")

    def test_load_from_browser(self):
        return load(self.test_path())

    def test_load_from_file(self):
        return load("bookmarks/bookmarks_2021_07_07.json")

    def test_bookmark_processing(self):
        bm = bookmarks(self.test_load_from_file(),
                       drop_local_files=False,
                       drop_duplicate_urls=False,
                       drop_directories=False)
        assert len(bm.bookmarks) == 1954

    def test_tags(self):
        print(bookmarks(self.test_load_from_browser()).bookmarks)

    def test_filters(self):
        print(bookmarks(self.test_load_from_browser(),
                        drop_directories=['Favorites bar', 'Other favorites']).bookmarks)
