import os
import toml
import datetime

from anchorage.bookmarks import bookmarks
from anchorage.anchor_tools.local import create_archive, add as add_local, server
from anchorage.anchor_tools.online import add as add_online
from anchorage.anchor_utils.system import home


def anchor_online(collection, overwrite,
                  loglevel=20):
    """
    Anchor all bookmarks in an online archive.

    :param collection: Bookmark JSON file or __bookmark__ class instance.
    :param loglevel: 0  - Full log output
                     20 - Progress bar
                     50 - Suppress all output

    :return: Dictionary with the name, url and error message of all bookmarks
             for which the archive process has failed.
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

    anchorage_error_log(err)


def anchor_locally(collection, archive="./anchor",
                   loglevel=20):
    """
    Archive all bookmarked pages in a local ArchiveBox archive.

    :param collection: Bookmark JSON file or __bookmark__ class instance.
    :param archive: Full path of chosen archive. Defaults to "/anchor".
    :param loglevel: 0  - Full log output
                     20 - Progress bar
                     50 - Suppress all output

    :return: Dictionary with the name, url and error message of all bookmarks
             for which the archive process has failed.
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

    anchorage_error_log(err)


def anchorage_error_log(error_log):
    """
    Save _anchor_online_ or _anchor_locally_ error log dictionary to

        ~/.anchorage/error_log_YYYY_MM_DD.toml

    :param error_log: List of bookmarks for which the upload process has failed.
    """
    anchorage_log = home() + f'/.anchorage/error_log_{datetime.datetime.now().strftime("%Y-%m-%d")}.toml'

    with open(anchorage_log, 'w') as log_file:
        toml.dump(error_log, log_file)


def anchor_error_log(where, archive="anchor"):
    """
    TODO: Attempt anchor of all bookmarks in the current error log.

    :param where:
    - 'online': archive online
    - 'local':  archive locally
    """
    create_archive(archive)

    pass


def anchor_log_online():
    """
    TODO: Attempt anchor of all bookmarks in the current error log.
    """
    pass
