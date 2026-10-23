"""
Line-by-line Python translation of ``week_08_practical_files/door_animation.java``.

The Java file is a JShell-style snippet rather than a class: it declares an
array of text blocks and then loops over them, clearing the terminal and
printing one frame every half second. The translation keeps the same five
frames and the same timing.

Java to Python mapping used here:

  ``String[] frames = { ... }``        -> a ``list[str]`` constant
  Java text block                      -> a triple-quoted string
  ``System.out.print("\\033[H\\033[2J")`` -> ``print(..., end="")``
  ``System.out.flush()``               -> ``sys.stdout.flush()``
  ``System.out.println(frame)``        -> ``print(frame)``
  ``Thread.sleep(500)``                -> ``time.sleep(0.5)``
  ``for (String frame : frames)``      -> ``for frame in FRAMES:``

Java text blocks do not include the newline that follows the opening
delimiter, while Python triple-quoted strings do. Each frame therefore calls
``lstrip("\\n")`` to remove exactly that one leading newline. The trailing
newline is kept, because Java's text block keeps the newline before the
closing delimiter as well.

The backslashes in the door art are doubled in the source (``\\\\``) so that
Python stores one backslash. A single backslash before a letter is an escape
sequence, and ``\\_`` is not a valid one; newer Pythons warn about it, which
would be noise for a drawing made of text.
"""

import sys
import time

# One frame per stage of the door opening: closed, half open, fully open,
# and then empty, which lets the animation end on a clean doorway.
FRAMES = [
    """
________
|   __   |
|  |  |  |
|  |  |  |
|  |__|  |
|        |
|________|
""".lstrip("\n"),
    """
 ________
|   __   |
|  |  |  |
|  |  |  |
|  |  |  |
|   \\ |  |
|____\\___|
""".lstrip("\n"),
    """
 ________
|   __   |
|   | |  |
|   | |  |
|   | |  |
|    \\|  |
|_____\\__|
""".lstrip("\n"),
    """
 ________
|        |
|     || |
|     || |
|     || |
|     || |
|______\\ |
""".lstrip("\n"),
    """
 ________
|        |
|        |
|        |
|        |
|        |
|_______ |
""".lstrip("\n"),
]

# 500 milliseconds, the value passed to Thread.sleep in the Java loop.
FRAME_DELAY_SECONDS = 0.5

# ANSI "home cursor" followed by "erase display". The two sequences are one
# string in Java and one string here; the terminal applies them in order.
CLEAR_SCREEN = "\033[H\033[2J"


def main() -> None:
    """
    Mirror of the Java loop below the ``frames`` array.

    ``System.out.print`` does not add a newline, so the escape sequence is
    written with ``end=""``. ``flush`` is needed because Python buffers
    redirected output; without it the first frame can appear late, which
    makes the animation look broken when it is only buffered.
    """
    for frame in FRAMES:
        print(CLEAR_SCREEN, end="")
        sys.stdout.flush()
        # Java's println adds the newline that separates one frame from the
        # next. The frame itself already ends with a newline.
        print(frame)
        time.sleep(FRAME_DELAY_SECONDS)


if __name__ == "__main__":
    main()

