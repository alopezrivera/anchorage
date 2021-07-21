import os
import sys
import shutil
import webbrowser

from Alexandria.general.console import print_color

from anchorage.anchor_utils.shell import shell, bckgr, raise_error, error, suppress_stdout
from anchorage.anchor_utils.aesthetic import smart_print_color


def archivebox(command_str):
    return shell(f"docker-compose run archivebox {command_str}")


def setup(archive):
    """
    Download ArchiveBox docker-compose.yml

    :param archive: Full path of archive directory
    """
    if not os.path.isdir(archive):
        os.mkdir(archive)
        os.chdir(archive)
    else:
        os.chdir(archive)

    docker_compose_yaml = "https://raw.githubusercontent.com/ArchiveBox/ArchiveBox/master/docker-compose.yml"
    if not os.path.isfile(f"{archive}/docker-compose.yml"):
        try:
            shell(f"curl -O {docker_compose_yaml}")
        except error():
            sys.exit("GNU wget and curl unavailable. Install any to proceed.")


def init(archive=None):
    """
    Creates ArchiveBox archive at dest

    :param archive: Full path of archive directory
    """
    if not isinstance(archive, type(None)):
        os.chdir(archive)

    archivebox("init --setup")


def create_archive(archive, overwrite=False):
    if os.path.isdir(archive):
        if overwrite:
            shutil.rmtree(archive)
            setup(archive=archive)
    else:
        setup(archive=archive)

    init(archive=archive)


def add(url, archive=None):
    """
    Adds website to archive in current directory, or a specified archive

    :param url: URL of website to be archived
    :param archive: Full path of archive directory
    """
    if not isinstance(archive, type(None)):
        os.chdir(archive)

    try:
        archivebox(f"add {url}")
    except:
        print("Error archiving: ", end="")
        print_color(url, "red")


def server(archive=None, browser_path=None, instakill=False):
    """
    Starts ArchiveBox server and opens it in browser of choice
    """

    if not isinstance(archive, type(None)):
        os.chdir(archive)

    p = bckgr("docker-compose up")  # Server

    browser = webbrowser.get(browser_path) if not isinstance(browser_path, type(None)) else webbrowser
    browser.open("http://127.0.0.1:8000")

    if not instakill:
        input("Click any key to close the server.")

    p.terminate()


def docker_check():
    with suppress_stdout():
        # Docker install check
        try:
            raise_error('docker')
        except error() as e:
            smart_print_color(f"Error: attempt to run 'docker' command in your shell failed. "
                              f"       Install Docker if you don't have it installed."
                              f"       Check your Docker installation by running 'docker --help' in your shell.",
                              'red')
            sys.exit()


def archivebox_check():
    with suppress_stdout():
        # ArchiveBox install check
        try:
            raise_error('archivebox')
        except error() as e:
            smart_print_color(f"Error: attempt to run 'archivebox' command in your shell failed. "
                              f"       Install ArchiveBox if you don't have it installed."
                              f"       Check your ArchiveBox installation by running 'archivebox' in your shell.",
                              'red')
            sys.exit()
