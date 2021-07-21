import unittest

from anchorage import add_online as add


class OnlineArchiveTests(unittest.TestCase):

    def test_add(self):
        print(add("http://paulgraham.com/think.html", "--ia", overwrite=True)[0])

    def test_existing(self):
        assert add("http://paulgraham.com/think.html", "--ia") == "Bookmark already present in the Internet Archive"
