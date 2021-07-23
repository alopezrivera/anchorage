import unittest

from anchorage.bookmarks import bookmarks, load, export, path

from Alexandria.general.console import print_color


class BookmarkTests(unittest.TestCase):

    def test_path(self):
        print("\nBOOKMARK TESTS: PATH\n")
        return path("edge beta")

    def test_export(self):
        print("\nBOOKMARK TESTS: EXPORT\n")
        return export(self.test_path(), "tests/bookmarks/exports")

    def test_load_from_browser(self):
        print("\nBOOKMARK TESTS: LOAD FROM BROWSER DATA\n")
        return load(self.test_path())

    def test_load_from_json(self):
        print("\nBOOKMARK TESTS: LOAD FROM JSON FILE\n")
        return load("tests/bookmarks/test_sample.json")

    def test_load_from_jsonlz4(self):
        print("\nBOOKMARK TESTS: LOAD FROM JSONLZ4 FILE\n")
        return load("tests/bookmarks/test_sample.jsonlz4")

    def test_bookmark_processing(self):
        print("\nBOOKMARK TESTS: ENSURE NO DATA IS LOST\n")
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
        print("\nBOOKMARK TESTS: BOOKMARK DIRECTORIES\n")
        print(bookmarks(self.test_load_from_browser()).bookmarks)

    def test_filter_string(self):
        print("\nBOOKMARK TESTS: STRING FILTER\n")
        print(bookmarks(self.test_load_from_browser(),
                        drop_dirs=['Favorites bar']))

    def test_filter_substring(self):
        print("\nBOOKMARK TESTS: SUBSTRING FILTER\n")
        print(bookmarks(self.test_load_from_browser(),
                        drop_dirs_subs=['Favorites']))

    def test_filter_regex(self):
        print("\nBOOKMARK TESTS: REGEX FILTER\n")
        print(bookmarks(self.test_load_from_browser(),
                        drop_names_regex=r'[aA]'))               # Match all names including 'a' or 'A'

    def test_loop(self):
        print("\nBOOKMARK TESTS: LOOP\n")
        bookmarks(load("tests/bookmarks/test_sample.json")).loop(lambda k, v: print_color((k, v), "green"),
                                                                 pb=False,
                                                                 suppress_output=False
                                                                 )

    def test_suppress_output(self):
        print("\nBOOKMARK TESTS: LOOP, SUPPRESSING OUTPUT\n")
        bookmarks(load("tests/bookmarks/test_sample.json")).loop(lambda k, v: print_color((k, v), "green"),
                                                                 pb=False,
                                                                 suppress_output=True
                                                                 )
