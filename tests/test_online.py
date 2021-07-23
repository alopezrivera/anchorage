import unittest

from anchorage import add_online as add


class OnlineArchiveTests(unittest.TestCase):

    def test_add(self):
        print("\nONLINE ARCHIVE TESTS: ADD NEW SITE\n")
        print(add("http://paulgraham.com/think.html", "--ia", overwrite=True)[0])

    def test_existing(self):
        print("\nONLINE ARCHIVE TESTS: AVOID SAVING IF ALREADY ARCHIVED\n")
        assert add("http://paulgraham.com/think.html", "--ia") == "Bookmark already present in the Internet Archive"
