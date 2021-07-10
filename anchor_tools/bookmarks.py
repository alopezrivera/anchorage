import os
import re
import toml
import shutil
import datetime
import rapidjson
from tqdm import tqdm

from Alexandria.general.project import root
from Alexandria.general.console import print_color

from anchor_infrs.ansi import colors
from anchor_infrs.system import operating_system
from anchor_infrs.shell import suppress_stdout
from anchor_infrs.infrastructure import init
from anchor_infrs.file_conversion import JSONLZ4_parser


def loc():
    return toml.load(init(True))


def path(browser):
    """
    :return: Path of browser of choice Bookmarks file
    """
    o_sys = operating_system()
    preamble = ("\\".join(str(os.getenv("APPDATA")).split("\\")[:-1])+"\\") if o_sys == "windows" else ""
    return preamble + loc()[browser][o_sys].replace("/", "\\")


print(loc())


def load(path):
    """
    :param path: Path to Bookmark JSON or JSONLZ4 file
    :return: Parsed JSON file
    """
    if path.split('\\')[-1].find('json') != -1:                    # Check if the JSON extension is present in path
        ext = path[len(path)-path[::-1].find('.'):].lower()        # If so obtain full extension
        if ext == "json":                                          # If full extension = JSON load normally
            return rapidjson.load(open(path, encoding="utf8"))
        elif ext == "jsonlz4":                                     # IF full extension = JSONLZ4 create bookmark
            d = rapidjson.loads(JSONLZ4_parser(path))              # dictionary appropriately
            bm_list = d['children'][0]['children']
            bm_dirs = [d['name'] for d in bm_list]
            bm_dics = [d for d in bm_list]
            return {'roots': dict(zip(bm_dirs, bm_dics))}
    else:                                                          # If no extension is present, the file is assumed
        return rapidjson.load(open(path, encoding="utf8"))         # to be a JSON file (the case for Chromium browsers)


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

        content = bookmark_dict['roots']

        self.bookmarks = {}
        self.tags = []
        self.n_dirs = 0

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
        if "children" in dictionary.keys():
            self.tags.append(dictionary['name'])            # Append directory name to tag list
            self.n_dirs += 1                                # Keep track of the number of directories
            self.search_children(dictionary['children'])    # Search through children
            self.tag_backtrack(dictionary['name'])          # After search is over, "navigate" back to parent directory

        elif 'url' in dictionary.keys():
            # Conduct a regex search for the name of the bookmark among all those previously found.
            #
            # Avoids a name conflict caused by the nth duplicate with n>1 due to the first
            # duplicate having already a different name to the first one, as
            #
            #       name of first duplicate = <name> ::anchorage name duplicate:: 2
            #
            n_rep = len(list(filter(re.compile(f"{re.escape(dictionary['name'])}").match,
                                    list(self.bookmarks.keys()))
                             ))
            #   1. re.escape
            #          Avoid issues with bookmarks with special regex sequences in their name
            #   2. re.compile(<bookmark name>
            #          Match any string with the entire bookmark name in it

            if n_rep > 0:
                key = dictionary['name'] + f" ::anchorage name duplicate:: {n_rep+1}"
            else:
                key = dictionary['name']

            self.bookmarks[key] = {"url": dictionary['url'],
                                   "tags": self.tags.copy()}
        else:
            pass        # Account for possibly empty bookmark folders

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

    def loop(self, f,
             pb=True,
             pb_label=None,
             pb_leave=True,
             pb_width=110,
             suppress_output=False
             ):
        """
        :param f: Function - To be run on each entry of the bookmark dictionary.
        :param pb: Boolean - True to visualize progress with tqdm progress bar.
        :param pb_label: Str - Progress bar label.
        :param pb_leave: Boolean - False to remove progress bar from screen after completion.
        :param pb_width: N - Width in char of the progress bar.
        :param suppress_output: Suppress output of the provided function.
        :return:
        """

        e = []

        if pb:                                          # Create tqdm progress bar if specified
            pgr = tqdm(self.bookmarks.items(),
                       ncols=pb_width,
                       position=0,
                       leave=pb_leave,
                       desc=pb_label,
                       bar_format="{l_bar}"
                                  "%s{bar}"
                                  "%s| {n_fmt}/{total_fmt} "
                                  "[{elapsed}<%s{remaining}%s,"
                                  " {rate_fmt}{postfix}]" % (colors.fgYellow, colors.reset,
                                                             colors.fgRed, colors.reset)
                       )

        for key, value in self.bookmarks.items():

            try:                                        # Attempt to run provided function on dictionary
                if suppress_output:
                    with suppress_stdout():             # Suppress function output if so specified
                        f(key, value)
                else:
                    f(key, value)
            except:                                     # Error: add entry to error list
                e.append([key, value])

            if pb:                                      # Update progress bar if in use
                pgr.update()

        print("\r" + " "*pb_width, end="\r")            # Clean console from debris left by tqdm

        return e

    def __repr__(self):
        links = []
        for key, value in self.bookmarks.items():
            links.append([key, value["url"]])

        lstr = "\n".join(" ".join(name_link) for name_link in links)
        info = f'\n\nFound: {len(self.bookmarks)} links and {self.n_dirs} directories.'

        return lstr + info
