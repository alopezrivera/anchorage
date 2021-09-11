# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Initialization and setup
------------------------
"""


import os
import toml

from anchorage.anchor_infrs.config import config
from anchorage.anchor_utils.system import home


def init(overwrite=False):
    """
    Initialize the Anchorage library

    1. Create ~/anchorage
    2. Save config.toml in /anchorage

    :param overwrite: Overwrite current config.toml if found
    """

    anchorage_dir = home() + '/.anchorage'
    anchorage_cfg = home() + '/.anchorage/config.toml'
    create_cfg = lambda: open(anchorage_cfg, 'w').write(config)

    install_status = check_install()

    if install_status == 0 and overwrite:
        create_cfg()
    if install_status == 1:
        create_cfg()
    if install_status == 2:
        os.mkdir(anchorage_dir)
        create_cfg()

    return anchorage_cfg


def check_install():
    """
    Check if

    1. ~/anchorage/ exists
    2. config.toml exists
    """
    anchorage_dir = home() + '/.anchorage'
    anchorage_cfg = home() + '/.anchorage/config.toml'

    if os.path.isdir(anchorage_dir):
        if os.path.isfile(anchorage_cfg) and os.stat(anchorage_cfg).st_size > 0:
            return 0
        else:
            return 1
    else:
        return 2


def read_config():
    anchorage_cfg = home() + '/.anchorage/config.toml'
    return toml.load(anchorage_cfg)
