# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Regex utilities
---------------
"""


import re
import sys

from alexandria.shell import print_color


def expr_check(expr):
    """
    Checks a given regex expression for correctness by compiling it
    and stopping execution if an error is raised.

    :param expr: Regex expression to be checked
    """
    try:
        re.compile(expr)
    except re.error:
        print_color("\n     Incorrect regex formula (regex compile error)\n", "red")
        sys.exit()
