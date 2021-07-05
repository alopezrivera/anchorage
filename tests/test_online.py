import unittest

from anchorage import add_online as add


class OnlineArchiveTests(unittest.TestCase):

    def test(self):
        add("https://superuser.com/questions/1291425/windows-subsystem-linux-make-vim-use-the-clipboard", "--ia")
