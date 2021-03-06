# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Anchorage config file
---------------------
"""


import codecs

config = codecs.decode(r'# Welcome to the                                                       \n'
                       r'#     /\              | |                                      | (_)   \n'
                       r'#    /  \   _ __   ___| |__   ___  _ __ __ _  __ _  ___     ___| |_|   \n'
                       r'#   / /\ \ |  _ \ / __|  _ \ / _ \|  __/ _  |/ _  |/ _ \   / __| | |   \n'
                       r'#  / ____ \| | | | (__| | | | (_) | | | (_| | (_| |  __/  | (__| | |   \n'
                       r'# /_/    \_\_| |_|\___|_| |_|\___/|_|  \__,_|\__, |\___|   \___|_|_|   \n'
                       r'#                                            __/ |                     \n'
                       r'#                                           |___/                      \n'
                       r'#                                                 Configuration file   \n'
                       r'#\n'
                       r'# Below you can see the path to the Bookmarks JSON/JSONLZ4 file for a  \n'
                       r'# series of browsers.\n'
                       r'# \n'
                       r'# Set your default browser to one of the available to skip browser     \n'
                       r'# choice when using the Anchorage CLI.                                 \n'
                       r'# \n'
                       r'# You can add new browsers and the path to their bookmarks file. You   \n'
                       r'# will then be able to set the new browser as the default, or choose   \n'
                       r'# it in the Anchorage CLI.                                             \n'
                       r'# \n'
                       r'# If using a custom browser **it must comply with the Chromium or      \n'
                       r'# Firefox bookmark storage conventions (i.e. dictionary key naming)**. \n'
                       r'# If this is not the case, export your bookmarks to a supported browser\n'
                       r'# and proceed.                                                         \n'
                       r'# \n'
                       r'# Path convention:                                                     \n'
                       r'#      Windows:            APPDATA/<your path>                         \n'
                       r'#      Linux, MacOS:       <full path>                                 \n'
                       r'# \n'
                       r'#                                           Antonio Lopez Rivera, 2021 \n'
                       r'\n'
                       r'[chrome]\n'
                       r'linux = "?"\n'
                       r'macos = "?"\n'
                       r'windows = "Local/Google/Chrome/User Data/Default/Bookmarks"\n'
                       r'\n'
                       r'[firefox]\n'
                       r'linux = "?"\n'
                       r'macos = "?"\n'
                       r'windows = "Roaming/Mozilla/Firefox/Profiles/mfeew61f.default-release/bookmarkbackups/"\n'
                       r'\n'
                       r'[edge]\n'
                       r'linux = "?"\n'
                       r'macos = "?"\n'
                       r'windows = "Local/Microsoft/Edge/User Data/Default/Bookmarks"\n'
                       r'\n'
                       r'["edge beta"]\n'
                       r'linux = "?"\n'
                       r'macos = "?"\n'
                       r'windows = "Local/Microsoft/Edge Beta/User Data/Default/Bookmarks"\n'
                       ,
                       'unicode_escape')

