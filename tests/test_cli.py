import unittest

from anchorage.cli import main


class CLITests(unittest.TestCase):

    def test_cli(self):
        print("\nCLI TESTS: MAIN\n")
        main()
