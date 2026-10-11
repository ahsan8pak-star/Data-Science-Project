"""
Box-drawing terminal output and input prompt.

Translation of ``TextUI.java``. The box geometry is preserved exactly:
the frame is four characters wider than the longest line, the title is
centred in the inner width, and body lines are left-padded with one
space.
"""

import sys


def box(title, lines=None, *more):
    """
    Print a bordered box with a centred title over the given lines.

    Accepts either a list of lines or variadic string arguments,
    mirroring the two Java overloads.
    """
    if lines is None:
        body = list(more)
    elif isinstance(lines, str):
        body = [lines, *more]
    else:
        body = list(lines) + list(more)
    width = max([len(title)] + [len(line) for line in body]) + 4
    rule = "-" * width
    print(rule)
    padding = (width - 2 - len(title)) // 2
    print("|" + " " * padding + title + " " * (width - 2 - padding - len(title)) + "|")
    print(rule)
    for line in body:
        print("| " + line + " " * (width - 3 - len(line)) + "|")
    print(rule)


def prompt(label, input_fn=None):
    """
    Print a label and return the stripped line typed after it.
    """
    reader = input_fn if input_fn is not None else input
    print(label, end=" ", flush=True)
    return reader().strip()


def eprint(*args):
    """
    Print to standard error, used for the crash handler.
    """
    print(*args, file=sys.stderr)

