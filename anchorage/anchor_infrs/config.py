config = '# Welcome to the\n' \
         '#     /\              | |                                      | (_)\n' \
         '#    /  \   _ __   ___| |__   ___  _ __ __ _  __ _  ___     ___| |_\n' \
         '#   / /\ \ |  _ \ / __|  _ \ / _ \|  __/ _  |/ _  |/ _ \   / __| | |\n' \
         '#  / ____ \| | | | (__| | | | (_) | | | (_| | (_| |  __/  | (__| | |\n' \
         '# /_/    \_\_| |_|\___|_| |_|\___/|_|  \__,_|\__, |\___|   \___|_|_|\n' \
         '#                                            __/ |\n' \
         '#                                           |___/\n' \
         '#                                                 Configuration file\n' \
         '#\n' \
         '# Below you can see the path to the Bookmarks JSON/JSONLZ4 file for a\n' \
         '# series of browsers.\n' \
         '# \n' \
         '# Set your default browser to one of the available to skip browser\n' \
         '# choice when using the Anchorage CLI. \n' \
         '# \n' \
         '# You can add new browsers and the path to their bookmarks file. You \n' \
         '# will then be able to set the new browser as the default, or choose\n' \
         '# it in the Anchorage CLI.\n' \
         '# \n' \
         '# If using a custom browser **it must comply with the Chromium or \n' \
         '# Firefox bookmark storage conventions (i.e. dictionary key naming)**.\n' \
         '# If this is not the case, export your bookmarks to a supported browser\n' \
         '# and proceed.\n' \
         '#                                           Antonio Lopez Rivera, 2021\n' \
         '\n' \
         '[chrome]\n' \
         'linux = "~/.config/google-chrome/Default/Bookmarks"\n' \
         'macos = "~/Library/Application Support/Google/Chrome/Default/Bookmarks"\n' \
         'windows = "Local/Google/Chrome/User Data/Default/Bookmarks"\n' \
         '\n' \
         '[edge]\n' \
         'linux = "?"\n' \
         'macos = "?"\n' \
         'windows = "Local/Microsoft/Edge/User Data/Default/Bookmarks"\n' \
         '\n' \
         '[firefox]\n' \
         'linux = "?"\n' \
         'macos = "?"\n' \
         'windows = "Roaming/Mozilla/Firefox/Profiles/mfeew61f.default-release/bookmarkbackups/" \n' \
         '\n' \
         '["edge beta"]\n' \
         'linux = "?"\n' \
         'macos = "?"\n' \
         'windows = "Local/Microsoft/Edge Beta/User Data/Default/Bookmarks"\n' \
         '\n' \
         '[defaults]\n' \
         'browser = "edge beta"\n' \
