import os

from anchorage.bookmarks import bookmarks
from anchorage.anchor_tools.local import create_archive, add as add_local, server
from anchorage.anchor_tools.online import add as add_online


def anchor_online(collection, overwrite,
                  loglevel=20):
    """
    Anchor all bookmarks in an online archive.

    :param collection: Bookmark JSON file or __bookmark__ class instance.
    :param loglevel: 0  - Full log output
                     20 - Progress bar
                     50 - Suppress all output
    """

    if isinstance(collection, bookmarks):
        err = collection.loop(lambda k, v: add_online(url=v["url"], overwrite=overwrite),
                              loglevel=loglevel,
                              pb_label="ARCHIVING",
                              )
    else:
        err = bookmarks(collection).loop(lambda k, v: add_online(url=v["url"], overwrite=overwrite),
                                         loglevel=loglevel,
                                         pb_label="ARCHIVING",
                                         )

    log_anchorage(err)


def anchor_locally(collection, archive="./anchor",
                   loglevel=20):
    """
    Archive all bookmarked pages in a local ArchiveBox archive.

    :param collection: Bookmark JSON file or __bookmark__ class instance.
    :param archive: Full path of chosen archive. Defaults to "/anchor".
    :param loglevel: 0  - Full log output
                     20 - Progress bar
                     50 - Suppress all output
    """

    create_archive(os.path.abspath(archive))

    if isinstance(collection, bookmarks):
        err = collection.loop(lambda k, v: add_local(url=v["url"]),
                              loglevel=loglevel,
                              pb_label="ARCHIVING",
                              )
    else:
        err = bookmarks(collection).loop(lambda k, v: add_local(url=v["url"]),
                                         loglevel=loglevel,
                                         pb_label="ARCHIVING",
                                         )

    log_anchorage(err)


def log_anchorage(error_log):
    """
    TODO: Save error log to ~/anchorage/error_log.toml

    :param error_log: List of bookmarks for which the upload process has failed.
    """
    print(error_log)


def anchor_log_locally(archive="anchor"):
    """
    TODO: Attempt anchor of all bookmarks in the current error log.
    """

    create_archive(archive)

    pass


def anchor_log_online():
    """
    TODO: Attempt anchor of all bookmarks in the current error log.
    """
    pass
