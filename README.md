# Anchorage

![alt text](tests/coverage/coverage.svg ".coverage available in tests/coverage/")

`Antonio Lopez Rivera, 2021`

## Table of Contents

[ **1. Introduction** ](#1-introduction)

[ **2. Install**  ](#2-install)

[ _2.1 Local archive: [ArchiveBox](https://archivebox.io/)_ ](#51-2d-lines)

[ _2.2 3D Lines_ ](#52-3d-lines)

## 1. Introduction

## 2. Install

    pip install anchorage

### 2.1 Local archive: [ArchiveBox](https://archivebox.io/)

1. Install docker
2. Install ArchiveBox via Docker

## 3. Usage

### 3.1 Bookmark retrieval

    from anchorage import load, path

### 3.2 Archive

    from anchorage import anchor_locally, anchor_online
    
    anchor_locally(bookmarks)
    
    anchor_online(bookmarks)

### 3.3 Local archive: ArchiveBox server

    from anchorage import server
    
    server()
