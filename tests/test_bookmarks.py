import os
import unittest

from anchorage.anchor_tools.bookmarks import bookmarks, load, export, path

from Alexandria.general.project import root
from Alexandria.general.console import print_color


class BookmarkTests(unittest.TestCase):

    def test_path(self):
        return path("edge beta")

    def test_export(self):
        return export(self.test_path(), "tests/bookmarks/exports")

    def test_load_from_browser(self):
        return load(self.test_path())

    def test_load_from_json(self):
        return load("tests/bookmarks/test_sample.json")

    def test_load_from_jsonlz4(self):
        return load("tests/bookmarks/test_sample.jsonlz4")

    def test_bookmark_processing(self):
        bm_chr = bookmarks(self.test_load_from_json(),
                           drop_local_files=False,
                           drop_duplicate_urls=False,
                           drop_dirs=False)
        bm_ffx = bookmarks(self.test_load_from_jsonlz4(),
                           drop_local_files=False,
                           drop_duplicate_urls=False,
                           drop_dirs=False)
        assert len(bm_chr.bookmarks) == 1954
        assert len(bm_ffx.bookmarks) == 1954

    def test_tags(self):
        print(bookmarks(self.test_load_from_browser()).bookmarks)

    def test_filter_string(self):
        print(bookmarks(self.test_load_from_browser(),
                        drop_dirs=['Favorites bar']))

    def test_filter_substring(self):
        print(bookmarks(self.test_load_from_browser(),
                        drop_dirs_subs=['Favorites']))

    def test_filter_regex(self):
        print(bookmarks(self.test_load_from_browser(),
                        drop_names_regex=r'[aA]'))               # Match all names including 'a' or 'A'

    def test_loop(self):
        bookmarks(load("tests/bookmarks/test_sample.json")).loop(lambda k, v: print_color((k, v), "green"),
                                                                 pb=False,
                                                                 suppress_output=False
                                                                 )
