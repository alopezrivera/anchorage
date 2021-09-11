# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

import unittest

from anchorage.cli import main


class CLITests(unittest.TestCase):

    def test_cli(self):
        print("\nCLI TESTS: MAIN\n")
        main()
