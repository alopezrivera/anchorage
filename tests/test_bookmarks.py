import unittest

from anchor_tools.bookmarks import bookmarks, load, export, path

from Alexandria.general.console import print_color


class BookmarkTests(unittest.TestCase):

    def test_path(self):
        return path("edge beta")

    def test_export(self):
        return export(self.test_path(), "tests/bookmarks")

    def test_load_from_browser(self):
        return load(self.test_path())

    def test_load_from_json(self):
        return load("tests/bookmarks/test_sample.json")

    def test_load_from_jsonlz4(self):
        return load("tests/bookmarks/bookmarks-2021-07-08_3004_QxMdZ4LDnLDAyJwxQvrelA==.jsonlz4")

    def test_bookmark_processing(self):
        bm_chr = bookmarks(self.test_load_from_json(),
                           drop_local_files=False,
                           drop_duplicate_urls=False,
                           drop_directories=False)
        bm_ffx = bookmarks(self.test_load_from_json(),
                           drop_local_files=False,
                           drop_duplicate_urls=False,
                           drop_directories=False)
        assert len(bm_chr.bookmarks) == 1954
        assert len(bm_ffx.bookmarks) == 1954

    def test_tags(self):
        print(bookmarks(self.test_load_from_browser()).bookmarks)

    def test_filters(self):
        print(bookmarks(self.test_load_from_browser(),
                        drop_directories=['Favorites bar', 'Other favorites']).bookmarks)

    def test_loop(self):
        bookmarks(load("tests/bookmarks/test_sample.json")).loop(lambda k, v: print_color((k, v), "green"),
                                                                 pb=False,
                                                                 suppress_output=True
                                                                 )
