import os
import shutil

from anchor_tools.bookmarks import path, load, bookmarks
from anchor_tools.local import create_archive, add as add_local, server
from anchor_tools.online import add as add_online


def anchor_locally(bookmark_file,
                   archive="anchor"):
    """
    Archive all bookmarked pages in a local ArchiveBox archive.

    :param bookmark_file: Bookmark JSON file.
    :param archive: Full path of chosen archive. Defaults to "/anchor".
    """

    create_archive(archive)

    bookmarks(bookmark_file).loop(lambda k, v: add_local(url=v["url"]))


def anchor_online(bookmark_file):
    """
    Anchor all bookmarks in an online archive.

    :param bookmark_file: Bookmark JSON file.
    """

    bookmarks(bookmark_file).loop(lambda k, v: add_online(url=v["url"]))
