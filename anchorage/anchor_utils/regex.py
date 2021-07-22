import re
import sys
from anchorage.anchor_utils.aesthetic import smart_print_color


def expr_check(expr):
    """
    Checks a given regex expression for correctness by compiling it
    and stopping execution if an error is raised.

    :param expr: Regex expression to be checked
    """
    try:
        re.compile(expr)
    except re.error:
        smart_print_color("\n     Incorrect regex formula (regex compile error)\n", "red")
        sys.exit()
