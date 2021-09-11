# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest

from anchorage.anchor_tools.online import add


class OnlineArchiveTests(unittest.TestCase):

    def test_add(self):
        print("\nONLINE ARCHIVE TESTS: ADD SITE\n")
        assert 'SUCCESS' in add("https://m.youtube.com/watch?v=XhExfYBfypI", "ia", overwrite=True)[0]

    def test_existing(self):
        print("\nONLINE ARCHIVE TESTS: AVOID SAVING IF ALREADY ARCHIVED\n")
        assert 'SKIPPED' in add("http://paulgraham.com/think.html", "ia")

    def test_exception(self):
        print("\nONLINE ARCHIVE TESTS: ATTEMPT SAVING FORBIDDEN BOOKMARK\n")
        assert 'FAILURE' in add("https://github.com/alopezrivera/WB3168-Robot-Mechanics", "ia")
