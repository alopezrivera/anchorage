import os
import shutil

from anchor_tools.bookmarks import path, load, loop
from anchor_tools.local import create_archive, add as add_local, server
from anchor_tools.online import add as add_online


def anchor_locally(bookmarks,
                   archive="anchor"):
    """
    Archive all bookmarked pages in a local ArchiveBox archive.

    :param bookmarks: Bookmark JSON file.
    :param archive: Full path of chosen archive. Defaults to "/anchor".
    """

    create_archive(archive)

    lambda x: add_local(url=x, archive=archive)


def anchor_online(bookmarks):
    """
    Anchor all bookmarks in an online archive.

    :param bookmarks: Bookmark JSON file.
    """
    add_local()