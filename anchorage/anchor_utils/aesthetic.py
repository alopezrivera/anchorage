from pyfiglet import Figlet

from alexandria.data_structs.string import join_set_distance
from alexandria.shell import print_color, str_log, str_color


def str_log_info(kind, msg):
    return str_log(kind, msg,
                   msg_color="", msg_bg_color="",
                   )


def str_log_success(msg):
    return str_log("SUCCESS", msg,
                   msg_color="brightCyan", msg_bg_color="",
                   kind_color="brightGreen", kind_bg_color=""
                   )


def str_log_error(msg):
    return str_log("FAILURE", msg,
                   msg_color="red", msg_bg_color="",
                   kind_color="brightRed", kind_bg_color=""
                   )


def str_log_progress(fraction, t_elapsed, t_remaining,
                     c_fr="brightCyan", c_bg_fr="",
                     c_te="", c_bg_te="",
                     c_tr="brightCyan", c_bg_tr="",
                     l=11, m=15, n=20):
    # Times
    def s_to_hms(_n):
        hours, remainder = divmod(_n, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f'{int(hours)}:{int(minutes)}:{seconds:.2f}'

    t_elapsed = s_to_hms(t_elapsed)
    t_remaining = "to go -> " + s_to_hms(t_remaining)

    # Set distances
    r = join_set_distance(fraction, "::", l)
    r = join_set_distance(r, t_elapsed, m)
    r = join_set_distance(r, " ::", n)
    r = join_set_distance(r, t_remaining, len(r)+2)

    str_t, str_kind, str_msg = r.split(" :: ")

    # Take care not to color whitespace for KIND string
    #     It is assumed that all possible whitespace has
    #     been added by <<join_set_distance>> and is thus
    #     placed at the end of the string.
    def countstrip(s):
        n0 = len(s)
        s = s.rstrip()
        n1 = len(str_kind)
        n_ws = n0 - n1
        return s, n_ws
    str_fraction, n_ws_fr = countstrip(fraction)
    str_te, n_ws_te = countstrip(t_elapsed)
    str_tr, n_ws_tr = countstrip(t_remaining)

    # Color
    c_str_fr    = str_color(str_t, c_fr, c_bg_fr) + " " * n_ws_fr
    c_str_te = str_color(str_kind, c_te, c_bg_te) + " " * n_ws_te
    c_str_tr  = str_color(str_msg, c_tr, c_bg_tr) + " " * n_ws_tr

    # Join in final string
    r = " :: ".join([c_str_fr, c_str_te, c_str_tr])
    return r


def newline():
    """
    Print an empty line. Purely for aesthetic reasons.
    """
    print("")


def title(text="Anchorage", font="big", color="cyan"):
    """
    Generates the Anchorage CLI title.

    :param text: Text to be rendered
    :param font: Figlet font to render the title
    :param color: Title color
    """
    f = Figlet(font=font)
    print_color(f.renderText(text), color)


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
