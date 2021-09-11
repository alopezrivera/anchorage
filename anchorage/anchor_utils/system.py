# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
System utilities
----------------
"""


import os
import platform


def operating_system():
    """
    :return: Operating system of host machine.
    """
    return platform.system().lower()


def home():
    """
    :return: Directory of file currently being run.
    """
    return os.environ['HOME']
