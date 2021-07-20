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
        bmk_dict = load(path(browser))
    else:
        bmk_dict = load(path(prompt(chrmm_path, style=style)['correctPath']))
elif browser == "firefox":
    bmk_dict = load(prompt(firefx_path, style=style)['path'])
else:
    bmk_dict = load(prompt(custom_path, style=style)['path'])
