import os
import shutil
import rapidjson
from Alexandria.general.project import root

from src.data.locs import locs


def load(path):
    """
    :param path: Path to Bookmark JSON
    :return: Parsed JSON file
    """
    return rapidjson.load(open(path, encoding="utf8"))


def export(path, dest=root() + "/bookmarks.json"):
    """
    :param path: Bookmark JSON path
    :param dest: Destination directory INCLUDING THE FILENAME
    :return: Export bookmark JSON file to the project's root directory
    """
    shutil.copyfile(path, dest)
    return dest


def path(sys, browser):
    """
    :param sys: Operating system
    :return: Path of browser of choice Bookmarks file
    """
    preamble = str(os.getenv("LOCALAPPDATA")) if sys == "windows" else ""
    return preamble + locs[browser][sys].replace("/", "\\")


def links(bookmarks):
    content = bookmarks["roots"]

    for directory in content:

        search_dict(content[directory])


def search_children(children):
    for child in children:
        search_dict(child)


def search_dict(dictionary):
    if list(dictionary.keys())[0] == "children":
        search_children(dictionary['children'])
    else:
        print(dictionary['name'], dictionary['url'])


links(load(path("windows", "edge beta")))
