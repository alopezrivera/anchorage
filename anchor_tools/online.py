from Alexandria.general.console import print_color

from anchor_tools.shell import shell


def add(url, archives=None):
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
    """

    flags = ' '.join(archives) if archives is list else archives if not isinstance(archives, type(None)) else ""

    try:
        shell(f"archivenow {flags} {url}")
    except:
        print("Error archiving: ", end="")
        print_color(url, "red")
