from internetarchive import get_item

from Alexandria.general.console import print_color

from anchor_tools.shell import shell


def add(url, archives=None, overwrite=False):
    """
    Archive a website in one of the four archives supported by Archive Now (archivenow).

    :param url: URL of website to be archived.
    :param archives: List or string of flags specifying in which archives to save the website.
                     Available flags:
                        - https://pypi.org/project/archivenow/
                     Example:
                        "all"
                        "--ia --is"
                        ["--ia", "--is"]
    :param overwrite: Archive URL even if it's already present in the Internet Archive.
    """

    def upload(url):
        flags = ' '.join(archives) if archives is list else archives if not isinstance(archives, type(None)) else ""
        try:
            copy = shell(f"archivenow {flags} {url}")
            return copy.stdout, copy.stderr
        except:
            print("Error archiving: ", end="")
            print_color(url, "red")

    if get_item(url).exists:
        if overwrite:
            return upload(url)
        else:
            return "Bookmark already present in the Internet Archive"
    else:
        return upload(url)
