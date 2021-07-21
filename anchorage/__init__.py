import os
import shutil

from anchor_tools.bookmarks import path, load, bookmarks
from anchor_tools.local import create_archive, add as add_local, server
from anchor_tools.online import add as add_online


def anchor_locally(collection,
                   archive="./anchor"):
    """
    Archive all bookmarked pages in a local ArchiveBox archive.

    :param collection: Bookmark JSON file or __bookmark__ class instance.
    :param archive: Full path of chosen archive. Defaults to "/anchor".
    """

    create_archive(archive)

    if isinstance(collection, bookmarks):
        err = collection.loop(lambda k, v: add_local(url=v["url"]),
                              pb_label="ARCHIVING",
                              suppress_output=True)
    else:
        err = bookmarks(collection).loop(lambda k, v: add_local(url=v["url"]),
                                         pb_label="ARCHIVING",
                                         suppress_output=True)

    log_anchorage(err)


def anchor_online(collection):
    """
    Anchor all bookmarks in an online archive.

    :param collection: Bookmark JSON file or __bookmark__ class instance.
    """

    if isinstance(collection, bookmarks):
        err = collection.loop(lambda k, v: add_online(url=v["url"]),
                              pb_label="ARCHIVING",
                              suppress_output=True)
    else:
        err = bookmarks(collection).loop(lambda k, v: add_online(url=v["url"]),
                                         pb_label="ARCHIVING",
                                         suppress_output=True)

    log_anchorage(err)


def log_anchorage(error_log):
    """
    Save error log to ~/anchorage/error_log.toml

    :param error_log: List of bookmarks for which the upload process has failed.
    """
    print(error_log)


def anchor_log_locally(archive="anchor"):
    """
    Attempt anchor of all bookmarks in the current error log.
    """

    create_archive(archive)

    pass


def anchor_log_online():
    """
    Attempt anchor of all bookmarks in the current error log.
    """
    pass
