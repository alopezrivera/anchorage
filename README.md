# Anchorage

![alt text](tests/coverage/coverage.svg ".coverage available in tests/coverage/")

As the internet ages, link rot takes over larger and larger swathes of it, bringing with it
the disappearance of courses, resources, interesting reads and more that we treasure. 
Anchorage is an attempt to let you save your little corner for good :)

Anchorage is a Python library and CLI to bulk archive your bookmark collection easily and
without friction. It allows you to retrieve your bookmark collection from your browser of 
choice, filter out duplicates, local files and entries matching string, substring and regex 
searches, and archive the whole thing: online in the [Internet Archive](https://archive.org/) 
or locally, using [ArchiveBox](https://archivebox.io/).

Read on for the Anchorage user's manual. The full Python API documentation is available 
in the [docs](https://anchorage-docs.github.io/) page.

`Antonio Lopez Rivera, 2021`

![alt text](https://github.com/antonlopezr/anchorage/blob/master/docs/demo/gifs/run.gif "Anchorage in action")

#### Table of Contents

[ 1. Introduction ](#1-introduction)

[ 3. Requirements & Install  ](#2-requirements--install)

[ 4. Anchorage configuration  ](#3-anchorage-configuration)

[ 4. Anchorage CLI  ](#4-anchorage-cli)

[ 6. Python API  ](#5-python-api)

[ _6.1 Anchorage configuration_ ](#51-anchorage-configuration)

[ _6.3 Bookmark retrieval_ ](#52-bookmark-retrieval)

[ _6.3 Archiving_ ](#53-archiving)

---

## 1. Introduction
What follows is the Anchorage user's manual. 

First it will deal with the requirements and install of the library, and then with its 
configuration, the Anchorage CLI and its Python API. A thorough documentation of each 
API method is available in the [docs](https://anchorage-docs.github.io/) site. 

## 2. Requirements & Install
A working [Docker](https://docs.docker.com/get-docker/) install is the only requirement, beyond Python and Anchorage's 
dependencies. 
**Without Docker**: Docker is used to run [ArchiveBox](https://archivebox.io/), via a provided 
[docker-compose file](https://github.com/ArchiveBox/ArchiveBox/wiki/Docker#docker-compose). 
Without Docker Anchorage will not be able to archive your collection locally, but it will still be 
able to save it online in the Internet Archive.

Anchorage can be installed using pip as any Python package. Its dependencies will be downloaded automatically. 

    pip install anchorage
    
## 3. Anchorage configuration
To access a browser's bookmarks file, Anchorage stores its location in its configuration file:

    ~/.anchorage/config.toml
    
There's an [example `config.toml`](https://github.com/antonlopezr/anchorage/blob/master/example-config.toml)
in this repo for reference. 

To add a new browser simply add a new top-level key, followed by its bookmark file paths. Anchorage only needs
the path in your operating system to work.

    [<browser name>]
    linux = <path>
    macos = <path>
    windows = <path>

Importantly:
- Linux and MacOS paths are stored in **full**.
- Windows paths are stored from the **`AppData`** directory.

The default `config.toml` contains the bookmark file paths for Google Chrome, Mozilla Firefox and Microsoft Edge
and Edge Beta for **Windows** only. To use Anchorage in **Linux or MacOS** add the bookmark file path of your
browser of choice to your `config.toml`.

#### Editing the Anchorage config file
The config file can be edited just as any other. 
New browsers will automatically be listed in the CLI.

Importantly:
- Set unknown bookmark file paths to "?". That way the CLI will recognize those as unknown and behave appropriately.

![alt text](https://github.com/antonlopezr/anchorage/blob/master/docs/demo/gifs/config.gif "Adding the location of the Google Chrome bookmarks file to ~/.anchorage/config.toml")

## 4. Anchorage CLI
The CLI will guide you through retrieving your bookmarks from your browser of choice, applying
filters to you bookmark collection and archiving your bookmarks in the Internet Archive or locally, 
using ArchiveBox.

To start the CLI open your shell and type

    anchorage

You will be asked whether you're ready to proceed. On the ok it will ensure all dependencies are present.

##### 1. Config check
If a config file is found, you will be prompted to choose whether to 
keep the current config or overwrite it with the default one.

##### 2. Browser choice
You will be prompted to choose which browser to retrieve your bookmark collection from. The browser 
choices are sourced from `config.toml`. Refer to [section 3](#3-anchorage-configuration) for 
editing it to add a missing browser or enter the path to the bookmarks file of your browser, if it's missing 
(equal to "?").

##### 3. Applying filters to the collection
Filters can be applied to your bookmark collection before archiving. 
Any or all of four filters can be chosen, one specific for URLs:

- `Local files`: remove local URLs (say, PDFs stored in your computer) from the collection.

and three general: 

- `Match string`: remove bookmark URLs, names or bookmark directories matching a provided string or any string 
in a string list.
- `Match substring`: remove bookmark URLs, names or bookmark directories containing a provided string or any string 
in a string list.
- `Regex`: remove bookmark URLs, names or bookmark directories matching a provided regex formula.

For each you will be prompted to choose to apply it to any or all of the previous.

##### 4. Archive choice
You will be then asked to choose whether to archive your collection online or locally.
##### _Online_
By default websites will not be archived if a previous image exists in The Internet Archive. This is to save time: we rest easy as a those 
sites are saved already at some point. In case you want to save a current snapshot of the colection, you will be prompted whether to override this 
and archive all sites in the collection regardless. This may take significantly longer. Based on your choice, you will be given an estimate of the 
archive time. 
##### _Local_
To archive your collection locally you will be prompted for an archive directory. 

##### 5. Run
After a last confirmation the process will begin. A progress bar will inform you of how far the process 
is from finishing, how many bookmarks have been saved and provide a dynamic estimate of the time remaining 
before the process is finished.

## 5. Python API: user's guide
The full documentation of the Anchorage API is available in the [docs](https://anchorage-docs.github.io/) site.

### 5.1 Anchorage configuration
Generate the Anchorage config file with the `init` command.

    from anchorage import init
    
    init()

### 5.2 Bookmark retrieval
Three methods are relevant:

- `path(<browser>)`: obtain the path to your chosen browser's bookmarks file (in your OS) from `config.toml`.
- `load(<path>)`: read your chosen browser's JSON or JSONLZ4 bookmarks file and return a Python dictionary.
- `bookmarks(<dict>)`: create an instance of the `bookmarks` class.

The `bookmarks` class creates a second bookmarks dictionary more suitable for our intent, and contains methods
to filter and loop through the collection. Filters can be applied as seen below.  

    from anchorage import path, load, bookmarks
    
    collection = bookmarks(load(path(<browser name>)),
                           drop_local_files= <boolean>,
                           drop_dirs=        <string or list of strings>,
                           drop_names=       <string or list of strings>,
                           drop_urls=        <string or list of strings>,
                           drop_dirs_subs=   <string or list of strings>,
                           drop_names_subs=  <string or list of strings>,
                           drop_urls_subs=   <string or list of strings>,
                           drop_dirs_regex=  <string>,
                           drop_names_regex= <string>,
                           drop_urls_regex=  <string>
                           )

### 5.3 Archiving
Input: `bookmarks` instance or bookmark dictionary returned by `load`. 

#### Online
The `overwrite` parameter determines whether to save snapshots of sites already present in the 
Internet Archive or not.

    from anchorage import anchor_online
    
    anchor_online(bookmarks, overwrite=<bool>)
    
#### Locally
The `archive` parameter specifies the directory in which to create the local archive.

    from anchorage import anchor_locally
    
    anchor_locally(bookmarks, archive=<dir>)

Running the [ArchiveBox](https://docs.archivebox.io/en/latest/README.html#web-ui-usage) default NGINX server 
can be done with the following command.

    from anchorage import server
    
    server()

---

[Back to top](#Anchorage)
