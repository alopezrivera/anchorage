# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
File conversion methods
-----------------------
"""


import re
import lz4.block


def JSONLZ4_to_JSON(path):
    """
    Turns a Firefox JSONLZ4 file into a string readable by `rapidjson`
    and with the same bookmark dictionary keys as those of Chromium
    browsers.

    :param path: Path to the JSONLZ4 file.
    """
    stream = open(path, 'rb')
    stream.read(8)                  # Skip b"mozLz40\0" header
    string = lz4.block.decompress(stream.read()).decode('utf-8')
    string = re.sub('title', 'name', string)
    string = re.sub('uri', 'url', string)
    return string
