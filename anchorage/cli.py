#!/usr/run/env python37

from __future__ import print_function, unicode_literals

import sys

from anchorage.bookmarks import bookmarks, path, load
from anchorage.anchor import anchor_online, anchor_locally
from anchorage.anchor_infrs.infrastructure import init, read_config
from anchorage.anchor_utils.shell import shell
from anchorage.anchor_utils.regex import expr_check
from anchorage.anchor_utils.aesthetic import smart_print_color, newline, title


try:
    from PyInquirer import style_from_dict, Token, prompt
except ImportError:
    print("PyInquirer import error: prompt-toolkits version != 1.0.14")
    print("Installing prompt-toolkit==1.0.14")
    shell("pip install prompt-toolkit==1.0.14")
    sys.exit("Success! Please run again")


def main():
    """
    # CLI interface for the Anchorage library.

    1. Dependency check
        - pip install --upgrade anchorage
        - check_install
    2. Browser choice
    3. Bookmark filter
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
    4. Local or online archive choice
        - Online
        - Local
            - Local archive directory input
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
        Token.Answer:           '#2196f3 bold',
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
        smart_print_color("\n     Operation cancelled\n", "red")
        sys.exit()

    smart_print_color("\n     ~Running dependency checks", "yellow")
    shell("pip3 install --upgrade anchorage")
    init()
    smart_print_color("     ~Everything in order!", "green")
    smart_print_color("     ~Edit configurations in ~/.anchorage/config.toml\n", "green")

    # 2. Browser choice
    cfg = read_config()

    brow_choice = [{
                    'type': 'list',
                    'name': 'browser',
                    'message': f'Please choose the browser from which to archive all bookmarks.',
                    'default': True,
                    'choices': list(cfg.keys()),
                    'filter': lambda n: n.lower()
                   }]

    bmk_dict = load(path(prompt(brow_choice, style=style)['browser']))
    newline()

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

    filter_kind = [{
                    'type': 'checkbox',
                    'name': 'kind',
                    'message': f'Specify filter targets.',
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
                                            'message': f'Enter a comma-separated list of {terms} to filter OUT.',
                                            'default': '',
                                            'filter': lambda string: string.split(",")
                                        }], style=style)['input']

    filter_regex = lambda terms: prompt([{
                                            'type': 'input',
                                            'name': 'input',
                                            'message': f'Enter regex formula to filter OUT {terms}.',
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
        kind = prompt(filter_kind, style=style)['kind']
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
        kind = prompt(filter_kind, style=style)['kind']
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
        kind = prompt(filter_kind, style=style)['kind']
        newline()
        if 'directories' in kind:
            drop_dir_regex = filter_regex('bookmark directory names')
            newline()
            expr_check(drop_dir_regex)
        if 'names' in kind:
            drop_name_regex = filter_regex('bookmark names')
            newline()
            expr_check(drop_name_regex)
        if 'urls' in kind:
            drop_url_regex = filter_regex('bookmark URLs')
            newline()
            expr_check(drop_url_regex)

    smart_print_color("     ~Applying filters to bookmark collection", "yellow")

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

    smart_print_color(f"     ~Done! Found {len(bmk.bookmarks)} bookmarks in {bmk.n_dirs} directories.\n", "green")

    # 4. Local or online archive
    archive_choice = [{
                    'type': 'list',
                    'name': 'archive',
                    'message': f'Choose an archiving method.',
                    'choices': ['Local (ArchiveBox)', 'Online'],
                    'filter': lambda n: n.split(' ')[0].lower()
                     }]

    archive = prompt(archive_choice, style=style)['archive']

    if archive == 'online':         # Anchor online
        anchor_online(bmk)

    if archive == 'local':          # Anchor locally

        dir_prompt = [{             # Archive directory input
                          'type': 'input',
                          'name': 'dir',
                          'message': 'Enter the full path of the archive directory (default: ./anchor).',
                          'default': './anchor'
                     }]
        archive_dir = prompt(dir_prompt, style=style)['dir']

        anchor_locally(bmk, archive_dir)
