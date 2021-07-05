import os
import shutil
import rapidjson
import numpy as np

from Alexandria.general.project import root

from anchor_tools.data.locs import locs


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


class links:

    def __init__(self, bookmarks,
                 drop_local_files=True,
                 banned_tags=None,
                 ):
        """
        Prepare bookmarks for archiving.

        :param bookmarks: Bookmark JSON file.
        """
        content = bookmarks["roots"]
        self.links = {}

        for directory in content:
            self.search_dict(content[directory])

    def search_dict(self, dictionary):
        """
        Reduce depth-n bookmark dictionary to depth-1 dictionary of -Name: Link - pairs.

        :param dictionary: Bookmark dictionary from which - Name: Link - pairs are to be extracted.
        :return: Depth-1 dictionary of - Name: Link - pairs.
        """
        if list(dictionary.keys())[0] == "children":
            self.search_children(dictionary['children'])
        else:
            self.links[dictionary['name']] = dictionary['url']

    def search_children(self, children):
        """
        Iterate over children.

        :param children: List entries in bookmark dictionary, which are by custom named "children" in
                         bookmark dictionaries.
        """
        for child in children:
            self.search_dict(child)

    def drop_local_files(self):
        pass


def loop(bookmarks):
    pass


print(links(load(path("windows", "edge beta"))).links)
