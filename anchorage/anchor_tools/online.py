from wayback import WaybackClient
from archivenow import archivenow

from alexandria.shell import print_color, suppress_stdout
from alexandria.shell.color import colors

from anchorage.anchor_utils.aesthetic import str_log_info, str_log_error, str_log_success


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
        try:
            if archive == 'cc':
                with suppress_stdout():
                    archive_url = archivenow.push(url, archive, api_key)[0]
            else:
                with suppress_stdout():
                    archive_url = archivenow.push(url, archive)[0]
            log = str_log_success(url + " -> -> -> " + archive_url)
            return log
        except BaseException as e:
            print(str_log_error(url))
            print_color(e, "red")

    try:
        archive_latest = next(WaybackClient().search(url))   # Search for URL using the WaybackMachine API
        if overwrite:
            return upload(url)
        else:
            return str_log_info("SKIPPED", url + " => => => " + archive_latest[7])
    except:
        # If bookmark search yields "0" error (defined by Python _wayback_)
        return upload(url)
