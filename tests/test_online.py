import unittest

from anchorage.anchor_tools.online import add


class OnlineArchiveTests(unittest.TestCase):

    def test_add(self):
        print("\nONLINE ARCHIVE TESTS: ADD NEW SITE\n")
        print(add("https://m.youtube.com/watch?v=XhExfYBfypI", "ia", overwrite=True)[0])

    def test_existing(self):
        print("\nONLINE ARCHIVE TESTS: AVOID SAVING IF ALREADY ARCHIVED\n")
        assert add("http://paulgraham.com/think.html", "ia") == "Bookmark already present in the Internet Archive"
