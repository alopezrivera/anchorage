import re
import sys
from anchorage.anchor_utils.aesthetic import smart_print_color


def expr_check(expr):
    try:
        re.compile(expr)
    except re.error:
        smart_print_color("\n     Incorrect regex formula (regex compile error)\n", "red")
        sys.exit()