from wayback import WaybackClient
from archivenow import archivenow

from alexandria.shell import suppress_stdout

from anchorage.anchor_utils.aesthetic import str_log_info, str_log_error, str_log_success


class UploadException(Exception):

    def __init__(self, message):
        super().__init__(message)


def add(url, archive='ia', api_key=None, overwrite=False):
    """
    Archive a website in one of the four archives supported by Archive Now (archivenow).

    TODO: Recognize internetarchive upload error messages as failures.

    :param url: URL of website to be archived.
    :param archive: List or string specifying archives to which to save the website.
                     Available archives:
                        - 'all': All archives
                        - 'ia': Internet Archive (default)
                        - 'is': Archive.is
                        - 'mg': Megalodon.jp
                        - 'cc': Perma.cc
    :param api_key: Perma.cc API key. Format:
                        {"cc_api_key":"$YOUR-Perma-cc-API-KEY"}
    :param overwrite: Archive URL even if it's already present in the Internet Archive.
    """

    def upload(url):
        if archive == 'cc':
            with suppress_stdout():
                archive_url = archivenow.push(url, archive, api_key)[0]
        else:
            with suppress_stdout():
                archive_url = archivenow.push(url, archive)[0]

        if "Error (The Internet Archive)" in archive_url:
            print(str_log_error(url + " ->/ ->/ ->/ " + archive_url))
            raise UploadException(archive_url)
        else:
            log = str_log_success(url + " -> -> -> " + archive_url)
        return log

    try:
        archive_latest = next(WaybackClient().search(url))   # Search for URL using the WaybackMachine API
        if overwrite:
            log = upload(url)
            print(log)
        else:
            log = str_log_info("SKIPPED", url + " => => => " + archive_latest[7])
            print(log)
    except StopIteration:
        # If bookmark search yields "0" error (defined by Python _wayback_)
        log = upload(url)
        print(log)
    except UploadException as e:
        return e
