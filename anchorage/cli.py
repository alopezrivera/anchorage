#!/usr/run/env python37
# SPDX-FileCopyrightText: © 2021 Antonio López Rivera <antonlopezr99@gmail.com>
# SPDX-License-Identifier: GPL-3.0-only

"""
Anchorage CLI
-------------
"""

from __future__ import print_function, unicode_literals

import sys

from alexandria.shell import print_color

from anchorage.bookmarks import bookmarks, path, load
from anchorage.anchor import anchor_online, anchor_locally
from anchorage.anchor_infrs.infrastructure import init, check_install, read_config
from anchorage.anchor_utils.shell import shell
from anchorage.anchor_utils.system import operating_system
from anchorage.anchor_utils.aesthetic import newline, title


try:
    from PyInquirer import style_from_dict, Token, prompt
except ImportError:
    print("PyInquirer import error: prompt-toolkits version != 1.0.14")
    print("Installing prompt-toolkit==1.0.14")
    shell("pip install prompt-toolkit==1.0.14")
    sys.exit("Success! Please run again")


def main():
    """
    # Anchorage library CLI.

    ## 1. Dependency check
        - Choice: overwrite config.toml if found
    ## 2. Browser choice
    ## 3. Bookmark filter
        - Local files
        - String match
            - Directories
            - Bookmark name
            - Bookmark URL
        - Substring match
            - Directories
            - Bookmark name
            - Bookmark URL
        - Regex match
            - Directories
            - Bookmark name
            - Bookmark URL
        - *Duplicate URLs are excluded by default*
    ## 4. Archive choice
        - Online
            - Skip sites already saved in TIA, or generate current snapshots for all sites in the collection
        - Local
            - Local archive directory input
    ## 5. Confirmation
    """

    # Title
    print('\nWelcome to the')
    title("Anchorage  cli")
    print("                                        Antonio Lopez Rivera, 2021\n")

    # CLI interface look
    style = style_from_dict({
        Token.QuestionMark:     '#E91E63 bold',
        Token.Selected:         '#673AB7 bold',
        Token.Instruction:      '',                # default
        Token.Answer:           '#9cdeff bold',
        Token.Question:         '',
    })

    """
    Dialogue
    """
    # 1. Dependency check
    dp_check = [{
                    'type': 'confirm',
                    'name': 'ready',
                    'message': 'Are you ready to proceed?',
                    'default': True
                }]

    if not prompt(dp_check, style=style)['ready']:
        print_color("\n     ~Operation cancelled\n", "red")
        sys.exit()

    print_color("\n     ~Running dependency checks", "white")
    shell("pip3 install --upgrade anchorage")

    if check_install() == 0:
        print("")
        reset_config = [{
            'type': 'confirm',
            'name': 'reset',
            'message': f'Previous config detected: reset config.toml?',
            'default': False,
        }]
        reset = prompt(reset_config, style=style)['reset']
        newline()
    else:
        reset = False

    init(reset)

    print_color("     ~Everything in order!", "green")
    print_color("     ~Edit configuration in ~/.anchorage/config.toml\n", "green")

    # 2. Browser choice
    cfg = read_config()
    brow_choice = [{
                    'type': 'list',
                    'name': 'browser',
                    'message': f'Please choose the browser from which to archive all bookmarks.',
                    'choices': list(map(lambda s: s.title(), list(cfg.keys()))),
                    'filter': lambda n: n.lower()
                   }]
    browser = prompt(brow_choice, style=style)['browser']
    newline()
    if cfg[browser][operating_system()] == "?":
        print_color("     ~The path to this browser hasn't been set up yet in your configuration file.", "red")
        print(f"     ~Edit ~/anchorage/config.toml to include the path for your {browser.title()} "
              f"bookmarks file and try again.\n")
        sys.exit()
    try:
        bmk_dict = load(path(browser))
    except FileNotFoundError:
        print_color("     ~Error: file not found.", "red")
        print_color("\n     ~Edit ~/anchorage/config.toml to include the correct bookmark file path "
                          "for your browser and try again.\n", "red")
        sys.exit()

    # 3. Bookmark filter
    #     - Local files
    #     - By string match
    #     - By substring match
    #     - By regex match
    bk_filt = [{
                    'type': 'checkbox',
                    'name': 'drop',
                    'message': f'If desired, specify which elements to exclude from the archiving process.',
                    'choices': [
                        {
                            'name': 'Local files'
                        },
                        {
                            'name': 'Match string'
                        },
                        {
                            'name': 'Match substring'
                        },
                        {
                            'name': 'Regex'
                        },
                    ],
                    'filter': lambda lst: [n.lower() if isinstance(n, str) else n for n in lst]
                  }]

    filter_kind = lambda kind: [{
                                    'type': 'checkbox',
                                    'name': 'kind',
                                    'message': f'Specify targets for {kind} filter.',
                                    'choices': [
                                        {
                                            'name': 'Directories'
                                        },
                                        {
                                            'name': 'Names'
                                        },
                                        {
                                            'name': 'URLs'
                                        },
                                    ],
                                    'filter': lambda lst: [n.lower() if isinstance(n, str) else n for n in lst]
                                }]

    filter_input = lambda terms: prompt([{
                                            'type': 'input',
                                            'name': 'input',
                                            'message': f'Enter a comma-separated list of {terms} to filter out.',
                                            'default': '',
                                            'filter': lambda string: string.split(",")
                                        }], style=style)['input']

    filter_regex = lambda terms: prompt([{
                                            'type': 'input',
                                            'name': 'input',
                                            'message': f'Enter regex formula to filter out {terms}.',
                                            'default': ''
                                         }], style=style)['input']

    drop_list = prompt(bk_filt, style=style)['drop']
    newline()

    drop_dirs       = None
    drop_names      = None
    drop_urls       = None
    drop_dir_subs   = None
    drop_name_subs  = None
    drop_url_subs   = None
    drop_dir_regex  = None
    drop_name_regex = None
    drop_url_regex  = None

    if 'match string' in drop_list:
        kind = prompt(filter_kind('string'), style=style)['kind']
        newline()
        if 'directories' in kind:
            drop_dirs = filter_input('bookmark directory names')
            newline()
        if 'names' in kind:
            drop_names = filter_input('bookmark names')
            newline()
        if 'urls' in kind:
            drop_urls = filter_input('bookmark URLs')
            newline()
    if 'match substring' in drop_list:
        kind = prompt(filter_kind('substring'), style=style)['kind']
        newline()
        if 'directories' in kind:
            drop_dir_subs = filter_input('bookmark directory name substrings')
            newline()
        if 'names' in kind:
            drop_name_subs = filter_input('bookmark name substrings')
            newline()
        if 'urls' in kind:
            drop_url_subs = filter_input('bookmark URL substrings')
            newline()
    if 'regex' in drop_list:
        kind = prompt(filter_kind('regex'), style=style)['kind']
        newline()
        if 'directories' in kind:
            drop_dir_regex = filter_regex('bookmark directory names')
            newline()
        if 'names' in kind:
            drop_name_regex = filter_regex('bookmark names')
            newline()
        if 'urls' in kind:
            drop_url_regex = filter_regex('bookmark URLs')
            newline()

    print_color("     ~Applying filters to bookmark collection", "white")

    bmk = bookmarks(bmk_dict,
                    drop_local_files='local files' in drop_list,
                    drop_dirs=drop_dirs,
                    drop_names=drop_names,
                    drop_urls=drop_urls,
                    drop_dirs_subs=drop_dir_subs,
                    drop_names_subs=drop_name_subs,
                    drop_urls_subs=drop_url_subs,
                    drop_dirs_regex=drop_dir_regex,
                    drop_names_regex=drop_name_regex,
                    drop_urls_regex=drop_url_regex,
                    )
    n_bookmarks = len(bmk.bookmarks)
    n_directories = bmk.n_dirs
    print_color(f"     ~Done! Found {n_bookmarks} bookmarks in {n_directories} directories.\n", "green")

    # 4. Archive choice
    archive_choice = [{
                    'type': 'list',
                    'name': 'archive',
                    'message': f'Choose an archiving method.',
                    'choices': ['Online', 'Local'],
                    'filter': lambda n: n.split(' ')[0].lower()
                     }]

    archive = prompt(archive_choice, style=style)['archive']
    newline()

    if archive == 'online':         # Online archive: save existing entries?
        print_color(f"     ~By default websites will not be archived if a previous image "
                          f"exists in The Internet Archive.\n", "white")
        ovw_online = [{
                          'type': 'confirm',
                          'name': 'overwrite',
                          'message': 'Save snapshots even if previous ones exist?',
                          'default': False
                     }]
        overwrite = prompt(ovw_online, style=style)['overwrite']
        newline()
        if overwrite:
            print_color(f"     ~Current snapshots will be saved for your entire collection. "
                              f"Expect a runtime of {n_bookmarks*15/3600:.2f} to {n_bookmarks*60/3600:.2f} "
                              f"hours.\n", "green")
        else:
            print_color(f"     ~Expect a runtime of {n_bookmarks*1.5/3600:.2f} to "
                              f"{n_bookmarks*3/3600:.2f} hours.\n", "green")
    if archive == 'local':          # Local archive directory
        dir_prompt = [{
                          'type': 'input',
                          'name': 'dir',
                          'message': 'Enter the relative or full path of the archive directory.',
                          'default': './anchor'
                     }]
        archive_dir = prompt(dir_prompt, style=style)['dir']
        newline()

    # 5. Log level
    log_prompt = [{
                        'type': 'list',
                        'name': 'loglevel',
                        'message': 'Enter the relative or full path of the archive directory.',
                        'choices': ['  - Full log output', '  - Progress bar', '  - Suppress all output'],
                        'filter': lambda choice: {'Full log output'    : 0,
                                                  'Progress bar'       : 20,
                                                  'Suppress all output': 50}[choice[4:]]
                  }]
    loglevel = prompt(log_prompt, style=style)['loglevel']
    newline()

    # 6. Confirmation
    confirmation = lambda br, nb: [{
                                        'type': 'confirm',
                                        'name': 'go',
                                        'message': 'All set! Proceed to archive your'
                                                   + " " + str(br) + " " + str(nb) + " " +
                                                   'bookmark collection?',
                                        'default': True
                                   }]
    conf_prompt = confirmation(browser.title(), n_bookmarks)

    go = prompt(conf_prompt, style=style)['go']
    newline()

    if go:
        if archive == 'online':                     # Anchor online
            anchor_online(bmk,
                          overwrite=overwrite,
                          loglevel=loglevel)
        elif archive == 'local':                    # Anchor locally
            anchor_locally(bmk,
                           archive=archive_dir,
                           loglevel=loglevel)
    else:
        print_color("     ~Operation cancelled\n", "red")
