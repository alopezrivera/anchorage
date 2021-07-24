# Anchorage

![alt text](tests/coverage/coverage.svg ".coverage available in tests/coverage/")

[Documentation](https://anchorage-docs.github.io/)

`Antonio Lopez Rivera, 2021`

## Table of Contents

[ **1. Introduction** ](#1-introduction)

[ **2. Install**  ](#2-install)

[ _2.1 Local archive: ArchiveBox_ ](#51-2d-lines)

[ **3. Anchorage CLI**  ](#3-anchorage-cli)

[ **4. Python library**  ](#4-python-library)

[ _4.1 Bookmark retrieval_ ](#41-bookmark-retrieval)

[ _4.3 The `bookmarks` class_ ](#42-the-bookmark-class)

[ _4.3 Archive_ ](#43-archive)

[ _4.3 Local archive: ArchiveBox server_ ](#43-local-archive-archivebox-server)

## 1. Introduction

## 2. Install

    pip install anchorage

### 2.1 [ArchiveBox](https://archivebox.io/)

1. Install docker
2. Install ArchiveBox via Docker

## 3. Anchorage CLI

![alt text](docs/screencaps/title.png)

#### Browser choice
<img src="docs/screencaps/br_choice.png" height="100">

#### Filter choice
![alt text](docs/screencaps/filter_choice.png | height=70)

##### Filter targets
![alt text](docs/screencaps/filter_targets.png | height=70)

##### String and substring filters
![alt text](docs/screencaps/filter_strings.png | height=70)

##### Regex filter
![alt text](docs/screencaps/filter_regex.png | height=70)

### Archive choice
![alt text](docs/screencaps/archive_choice.png | height=70)

#### Local: directory choice
![alt text](docs/screencaps/local_path.png)

#### Online: save current snapshots
![alt text](docs/screencaps/overwrite.png)

![alt text](docs/screencaps/exp_runtime.png)

#### 

## 4. Python library

### 4.1 Bookmark retrieval

    from anchorage import load, path
    
### 4.2 The `bookmarks` class

### 4.3 Archive

    from anchorage import anchor_locally, anchor_online
    
    anchor_locally(bookmarks)
    
    anchor_online(bookmarks)

#### 4.3.1 Local archive: [ArchiveBox](https://archivebox.io/) server

    from anchorage import server
    
    server()
