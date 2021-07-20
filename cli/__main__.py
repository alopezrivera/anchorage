from __future__ import print_function, unicode_literals

import sys
from pyfiglet import Figlet

from anchorage import anchor_online, anchor_locally, bookmarks, path, load
from anchor_infrs.infrastructure import init, read_config
from anchor_utils.shell import shell
from anchor_utils.regex import expr_check
from anchor_utils.aesthetic import smart_print_color, newline


try:
    from PyInquirer import style_from_dict, Token, prompt
except ImportError:
    print("PyInquirer import error: prompt-toolkits version != 1.0.14")
    print("Installing prompt-toolkit==1.0.14")
    shell("pip install prompt-toolkit==1.0.14")
    sys.exit("Success! Please run again")


def title(text="Anchorage", font="big", color="yellow"):
    f = Figlet(font=font)
    smart_print_color(f.renderText(text), color)


def interface():
    """
    CLI interface for the Anchorage library.

    Dialogue:
        1. Dependency check
            - pip install --upgrade anchorage
            - check_install
        2. OS check
        3. Browser choice
        4. Browser Bookmark file path check
            - Return known Bookmark file path, ask user to confirm
            - Read bookmark file
                - Positive confirmation
                - Negative confirmation, back to step 4. or exit
        5. Bookmark filter
            - Exclude local files
            - Exclude certain directories
            - Exclude bookmarks with given strings within their names
            - Exclude bookmarks with given strings within their links
        6. Local or online archive
            6.1 Local
                6.1.1 Docker install check
                    - Provide link to user if Docker is not installed
                6.1.2 Local archive directory input
                    - Check full path of local archive path with user
        7. Ready to go!
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
    # shell("pip3 install --upgrade anchorage")
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
                    'choices': list(cfg.keys())[:-1],
                    'filter': lambda n: n.lower()
                   }]

    bmk_dict = load(path(prompt(brow_choice, style=style)['browser']))
    newline()

    # 5. Bookmark filter
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
                                            'message': f'Enter a comma-separated list of the {terms} to filter.',
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

    if 'match string' in drop_list:
        kind = prompt(filter_kind, style=style)['kind']
        newline()
        if 'directories' in kind:
            drop_dirs = filter_input('directories')
            newline()
        if 'names' in kind:
            drop_names = filter_input('names')
            newline()
        if 'urls' in kind:
            drop_urls = filter_input('URLs')
            newline()
    if 'match substring' in drop_list:
        kind = prompt(filter_kind, style=style)['kind']
        newline()
        if 'directories' in kind:
            drop_dir_subs = filter_input('directory substrings')
            newline()
        if 'names' in kind:
            drop_name_subs = filter_input('name substrings')
            newline()
        if 'urls' in kind:
            drop_url_subs = filter_input('URL substrings')
            newline()
    if 'regex' in drop_list:
        kind = prompt(filter_kind, style=style)['kind']
        newline()
        if 'directories' in kind:
            drop_dir_regex = filter_regex('bookmark directories')
            newline()
            expr_check(drop_dir_regex)
        if 'names' in kind:
            drop_name_regex = filter_regex('bookmark names')
            newline()
            expr_check(drop_name_regex)
        if 'urls':
            drop_url_regex = filter_regex('bookmark URLs')
            newline()
            expr_check(drop_url_regex)

    # bmk = bookmarks(bmk_dict,
    #                 drop_local_files='local files' in drop_list,
    #                 drop_dirs=drop_dirs,
    #                 drop_names=drop_names,
    #                 drop_urls=drop_urls,
    #                 drop_dir_if_contains=drop_dir_subs,
    #                 drop_name_if_contains=drop_name_subs,
    #                 drop_url_if_contains=drop_url_subs,
    #                 drop_dir_regex=drop_dir_regex,
    #                 drop_name_regex=drop_name_regex,
    #                 drop_url_regex=drop_url_regex,
    #                 )

    # 6. Local or online archive
    #     6.1 Local
    #         6.1.1 Docker install check
    #             - Provide link to user if Docker is not installed
    #         6.1.2 Local archive directory input
    #             - Check full path of local archive path with user

    archive_choice = [{
                    'type': 'list',
                    'name': 'archive',
                    'message': f'Choose an archiving method.',
                    'choices': ['Local (ArchiveBox)', 'Online'],
                    'filter': lambda lst: [n.split(' ')[0].lower() if isinstance(n, str) else n for n in lst]
                  }]
    archive = prompt(archive_choice, style=style)




interface()
