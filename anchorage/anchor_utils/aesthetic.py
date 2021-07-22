from pyfiglet import Figlet

from Alexandria.general.console import print_color

from anchorage.anchor_utils.system import operating_system


def smart_print_color(text, color, **kwargs):
    """
    Print in color in UNIX terminals, and use the regular `print` function
    elsewhere.

    :param text: Text to be printed to screen
    :param color: Text color
    :param kwargs: Any further keyword arguments for the `print` function
    """
    if operating_system() in ["linux", "macos"]:
        print_color(text, color, **kwargs)
    else:
        print(text, **kwargs)


def newline():
    """
    Print an empty line. Purely for aesthetic reasons.
    """
    print("")


def title(text="Anchorage", font="big", color="yellow"):
    """
    Generates the Anchorage CLI title.

    :param text: Text to be rendered
    :param font: Figlet font to render the title
    :param color: Title color
    """
    f = Figlet(font=font)
    smart_print_color(f.renderText(text), color)


class colors:
    """
    ANSI color codes for use with `tqdm` to generate colored progress bars.
    """

    reset = "\033[0m"

    # Black
    fgBlack = "\033[30m"
    fgBrightBlack = "\033[30;1m"
    bgBlack = "\033[40m"
    bgBrightBlack = "\033[40;1m"

    # Red
    fgRed = "\033[31m"
    fgBrightRed = "\033[31;1m"
    bgRed = "\033[41m"
    bgBrightRed = "\033[41;1m"

    # Green
    fgGreen = "\033[32m"
    fgBrightGreen = "\033[32;1m"
    bgGreen = "\033[42m"
    bgBrightGreen = "\033[42;1m"

    # Yellow
    fgYellow = "\033[33m"
    fgBrightYellow = "\033[33;1m"
    bgYellow = "\033[43m"
    bgBrightYellow = "\033[43;1m"

    # Blue
    fgBlue = "\033[34m"
    fgBrightBlue = "\033[34;1m"
    bgBlue = "\033[44m"
    bgBrightBlue = "\033[44;1m"

    # Magenta
    fgMagenta = "\033[35m"
    fgBrightMagenta = "\033[35;1m"
    bgMagenta = "\033[45m"
    bgBrightMagenta = "\033[45;1m"

    # Cyan
    fgCyan = "\033[36m"
    fgBrightCyan = "\033[36;1m"
    bgCyan = "\033[46m"
    bgBrightCyan = "\033[46;1m"

    # White
    fgWhite = "\033[37m"
    fgBrightWhite = "\033[37;1m"
    bgWhite = "\033[47m"
    bgBrightWhite = "\033[47;1m"
