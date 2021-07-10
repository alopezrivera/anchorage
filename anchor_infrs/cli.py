from __future__ import print_function, unicode_literals

import sys
import platform
from pyfiglet import Figlet
from PyInquirer import style_from_dict, Token, prompt

from Alexandria.general.console import print_color

from anchorage import anchor_online, anchor_locally, path, load
from anchor_infrs.infrastructure import init
from anchor_infrs.system import operating_system
from anchor_infrs.shell import shell


def smart_print_color(text, color, **kwargs):
    if operating_system() in ["linux", "macos"]:
        print_color(text, color, **kwargs)
    else:
        print(text, **kwargs)


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
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })

    """
    Dialogue
    """
    # 1. Dependency check
    #     - pip install --upgrade anchorage
    #     - check_install
    dp_check = [{
                    'type': 'confirm',
                    'name': 'ready',
                    'message': 'Are you ready to proceed?',
                    'default': True
                }]

    if not prompt(dp_check, style=style)['ready']:
        smart_print_color("\n     Operation cancelled\n", "red")
        sys.exit()

    print("  ~~Running dependency checks")
    # shell("pip3 install --upgrade anchorage")
    init()
    print("  ~~Everything in order! Edit browser settings in ~/.anchorage/config.toml")

    # 2. Browser choice
    brow_choice = [{
                    'type': 'list',
                    'name': 'browser',
                    'message': f'Please choose the browser from which to archive all bookmarks.',
                    'default': True,
                    'choices': ['Chrome', 'Firefox', 'Edge', 'Other'],
                    'filter': lambda n: n.lower()
                   }]
    firefx_path = [{
                      'type': 'input',
                      'name': 'path',
                      'message': 'Please input the full path (with FILENAME.JSONLZ4) '
                                 'of your latest Firefox bookmark backup.',
                      'default': ''
                   }]
    custom_path = [{
                      'type': 'input',
                      'name': 'path',
                      'message': "Please input the full path (with FILENAME.EXT)"
                                 "of your browser's JSON or JSONLZ4 bookmarks file.\n"
                                 "  It must comply with the Chromium (JSON) or Firefox (JSONLZ4) "
                                 "bookmark storage conventions.\n"
                                 "  If loading is unsuccessful, export your bookmarks to a "
                                 "supported browser and attempt again.\n",
                      'default': ''
                   }]

    browser = prompt(brow_choice, style=style)['browser']

    if browser in ["chrome", "edge"]:
        chrmm_check = [{
            'type': 'confirm',
            'name': 'correctPath',
            'message': f"\n\n    {path(browser)}\n\n  Is this path to your browser's Bookmark file correct?",
            'default': True
        }]
        chrmm_path = [{
            'type': 'input',
            'name': 'correctPath',
            'message': f"Please input the correct path to your browser's Bookmark file.\n",
            'default': True
        }]
        if prompt(chrmm_check, style=style)['correctPath']:
            bmk = load(path(browser))
        else:
            bmk = load(path(prompt(chrmm_path, style=style)['correctPath']))
    elif browser == "firefox":
        bmk = load(prompt(firefx_path, style=style)['path'])
    else:
        bmk = load(prompt(custom_path, style=style)['path'])

#     # 5. Bookmark filter
#     #     - Exclude local files
#     #     - Exclude certain directories
#     #     - Exclude bookmarks with given strings within their names
#     #     - Exclude bookmarks with given strings within their links
#     bk_filt = []
#     prompt(bk_filt, style=style)
#     # 6. Local or online archive
#     archive = []
#     prompt(archive, style=style)
#     #     6.1 Local
#     #         6.1.1 Docker install check
#     #             - Provide link to user if Docker is not installed
#     #         6.1.2 Local archive directory input
#     #             - Check full path of local archive path with user
#     a_local = []
#     prompt(a_local, style=style)
#
#
# questions = [
#         {
#             'type': 'confirm',
#             'name': 'toBeDelivered',
#             'message': 'Is this for delivery?',
#             'default': False
#         },
#         {
#             'type': 'input',
#             'name': 'phone',
#             'message': 'What\'s your phone number?',
#             'validate': PhoneNumberValidator
#         },
#         {
#             'type': 'list',
#             'name': 'size',
#             'message': 'What size do you need?',
#             'choices': ['Large', 'Medium', 'Small'],
#             'filter': lambda val: val.lower()
#         },
#         {
#             'type': 'input',
#             'name': 'quantity',
#             'message': 'How many do you need?',
#             'validate': NumberValidator,
#             'filter': lambda val: int(val)
#         },
#         {
#             'type': 'expand',
#             'name': 'toppings',
#             'message': 'What about the toppings?',
#             'choices': [
#                 {
#                     'key': 'p',
#                     'name': 'Pepperoni and cheese',
#                     'value': 'PepperoniCheese'
#                 },
#                 {
#                     'key': 'a',
#                     'name': 'All dressed',
#                     'value': 'alldressed'
#                 },
#                 {
#                     'key': 'w',
#                     'name': 'Hawaiian',
#                     'value': 'hawaiian'
#                 }
#             ]
#         },
#         {
#             'type': 'rawlist',
#             'name': 'beverage',
#             'message': 'You also get a free 2L beverage',
#             'choices': ['Pepsi', '7up', 'Coke']
#         },
#         {
#             'type': 'input',
#             'name': 'comments',
#             'message': 'Any comments on your purchase experience?',
#             'default': 'Nope, all good!'
#         },
#         {
#             'type': 'list',
#             'name': 'prize',
#             'message': 'For leaving a comment, you get a freebie',
#             'choices': ['cake', 'fries'],
#             'when': lambda answers: answers['comments'] != 'Nope, all good!'
#         }
#     ]

interface()
