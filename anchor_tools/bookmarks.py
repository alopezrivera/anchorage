import os
import re
import shutil
import datetime
import rapidjson

from Alexandria.general.project import root
from Alexandria.general.console import print_color

from anchor_tools.data.locs import locs


def path(sys, browser):
    """
    :param sys: Operating system
    :return: Path of browser of choice Bookmarks file
    """
    preamble = str(os.getenv("LOCALAPPDATA")) if sys == "windows" else ""
    return preamble + locs[browser][sys].replace("/", "\\")


def load(path):
    """
    :param path: Path to Bookmark JSON
    :return: Parsed JSON file
    """
    return rapidjson.load(open(path, encoding="utf8"))


def export(path, dest=root()):
    """
    :param path: Bookmark JSON path
    :param dest: Destination directory INCLUDING THE FILENAME
    :return: Export bookmark JSON file to the project's root directory
    """
    date = datetime.datetime.today().strftime('%Y_%m_%d')
    filename = f"/bookmarks_{date}.json"
    shutil.copyfile(path, dest + filename)
    return dest


class bookmarks:

    def __init__(self, bookmark_dict,
                 drop_local_files=True,
                 drop_duplicate_urls=True,
                 drop_directories=None,
                 ):
        """
        Prepare bookmarks for archiving.

        Instance attributes:

            self.links: dictionary of - Name: Dict - pairs, where

                Dict: {"url": url,
                       "tags": [tag_1, tag_2, ..., tag_n]}

            self.tags: list containing the ordered names of the parent folders of each link.

        :param bookmark_dict: Bookmark JSON file.
        :param drop_local_files: Remove local file bookmarks from bookmark list.
        :param drop_duplicate_urls: Remove duplicated URLs.
        :param drop_directories: Directories from which no bookmarks are to be archived.
        """
        content = bookmark_dict["roots"]
        self.bookmarks = {}
        self.tags = []
        self.n_dirs = 0

        self.test = 0
        self.diff = 0

        # Conduct iteration
        for directory in content:
            self.search_dict(content[directory])        # Iteration
            self.tags = []                              # "Navigate" back to root
            self.n_dirs += 1                            # Keep track of the number of directories

        # Remove local files from dictionary
        if drop_local_files:
            self.drop_local_files()
        # Drop duplicate links
        if drop_duplicate_urls:
            self.drop_duplicate_urls()
        # Remove unwanted directories
        if drop_directories:
            self.drop_directories(unwanted_directories=drop_directories)

    def search_dict(self, dictionary):
        """
        Reduce depth-n bookmark dictionary to depth-1 dictionary of -Name: Dict - pairs, where

            Dict: {"url": url,
                   "tags": tag_list}

        and tag_list is a list containing the ordered names of the parent folders of each link.

        :param dictionary: Bookmark dictionary from which - Name: [link, tags] - pairs are to be extracted.
        :return: Depth-1 dictionary of - Name: [link, tags] - pairs.
        """
        if list(dictionary.keys())[0] == "children":
            print("\n", dictionary['name'])
            self.tags.append(dictionary['name'])            # Append directory name to tag list
            self.n_dirs += 1                                # Keep track of the number of directories
            self.search_children(dictionary['children'])    # Search through children
            self.tag_backtrack(dictionary['name'])          # After search is over, "navigate" back to parent directory
        else:

            # Conduct a regex search for the name of the bookmark:
            #       1. Escape back
            n_rep = len(list(filter(re.compile(f"{re.escape(dictionary['name'])}").match,
                                    list(self.bookmarks.keys()))))
            # n_rep = len(list(filter(lambda x: x.find(dictionary['name']),
            #                         list(self.bookmarks.keys()))))

            if n_rep > 0:
                key = dictionary['name'] + f" ::anchorage name duplicate:: {n_rep+1}"
            # elif dictionary['url'] in list([bookmark['url'] for bookmark in self.bookmarks.values()]):
            #     n_rep = list([bookmark['url'] for bookmark in self.bookmarks.values()]).count(dictionary['url'])
            #     key = dictionary['name'] + f" ::anchorage url duplicate:: {n_rep + 1}"
            else:
                key = dictionary['name']

            self.test += 1

            self.bookmarks[key] = {"url": dictionary['url'],
                                   "tags": self.tags.copy()}

            if n_rep > 0:
                print_color("??????????????????????????????????????????????", "green")
                print_color(list(self.bookmarks.keys())[-1], "green")
                print_color(self.bookmarks[list(self.bookmarks.keys())[-1]], "green")
                print_color("??????????????????????????????????????????????", "green")

            print(self.test, abs(len(self.bookmarks) - self.test))

            if abs(len(self.bookmarks) - self.test) > abs(self.diff):
                print_color("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", "red")
                print_color(dictionary['name'], "red")
                print_color(list(filter(re.compile(f".*{dictionary['name']}").match,
                                        list(self.bookmarks.keys()))), 'red')
                print(len(self.bookmarks), self.test)
                print_color(key, "red")
                print_color(self.bookmarks[key], "red")
                print(key in list(self.bookmarks.keys()))
                print(dictionary['url'] in list([bookmark['url'] for bookmark in self.bookmarks.values()]))
                print_color(self.bookmarks[list(self.bookmarks.keys())[-1]], "red")
                print_color("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", "red")
                self.diff = len(self.bookmarks) - self.test

    def search_children(self, children):
        """
        Iterate over children.

        :param children: List entries in bookmark dictionary, which are by custom named "children" in
                         bookmark dictionaries.
        """
        for child in children:
            self.search_dict(child)

    def tag_backtrack(self, tag):
        """
        Remove tracked tags deeper than input tag.
            For a series of nested dictionaries (D) which may contain "children" lists (c)

                D
                |_ c[dir_name1]             tags = [dir_name1]
                   |_ D
                   |  |_ c[dirname_2]       tags = [dir_name1, dir_name2]
                   |     |_ D
                   |_ D                  !! tags = [dir_name1]

            It is necessary to be able to "navigate" to the current parent directory after
            iterating through any subdirectories.

            The "path" to each link is kept in an ordered list. To "navigate" back after
            iterating through any previously subdirectories, all elements in the tag list
            after the specified (parent) tag are eliminated.
        """
        try:
            inv_index = self.tags[::-1].index(tag)
            index = len(self.tags) - 1 - inv_index
            self.tags = self.tags[:index]
        except ValueError:
            self.tags = [tag]

    def drop_duplicate_urls(self):
        links = []
        for key, value in self.bookmarks.copy().items():
            if value['url'] in links:
                del self.bookmarks[key]
            else:
                links.append(value['url'])

    def drop_local_files(self):
        for key, value in self.bookmarks.copy().items():
            if "http" not in value["url"][:4]:
                del self.bookmarks[key]

    def drop_directories(self, unwanted_directories):
        if isinstance(unwanted_directories, str):
            unwanted_directories = [unwanted_directories]

        for key, value in self.bookmarks.copy().items():
            if list(set(unwanted_directories) & set(list(value["tags"]))):
                del self.bookmarks[key]

    def loop(self, f):
        for key, value in self.bookmarks.items():
            f(key, value)

    def __repr__(self):
        links = []
        for key, value in self.bookmarks.items():
            links.append([key, value["url"]])

        lstr = "\n".join(" ".join(name_link) for name_link in links)
        info = f'\n\nFound: {len(self.bookmarks)} links and {self.n_dirs} directories.'

        return lstr + info
