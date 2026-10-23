"""
Line-by-line Python translation of ``week_03_lecture_code/FallBall.java``.

The Java program animates a ball falling under gravity in a 20-row
terminal. Each frame it moves the cursor home, draws exactly one ``O`` at
the ball's row, and sleeps for 60 milliseconds.

Java to Python mapping used here:

  ``String hide = "\\033[?25l"``     -> an ANSI escape string (hide cursor)
  ``String erase = "\\033[2J"``      -> an ANSI escape string (clear screen)
  ``String home = "\\033[H"``        -> an ANSI escape string (cursor home)
  ``Thread.sleep(60)``              -> ``time.sleep(0.06)`` (60 ms)
  ``(int) height``                  -> ``int(height)`` (truncates toward 0)
  ``while (true)``                  -> ``while True:``

The escape codes are terminal control sequences, not text to print. They
only work in a terminal that understands ANSI; a Jupyter notebook shows
them as stray characters, so run this script from a shell.

The casting difference matters: Java's ``(int)`` truncates toward zero and
Python's ``int()`` does the same for positive numbers, so the row numbers
match the Java program exactly.
"""

import time

# ANSI control sequences. "print" sends them to the terminal, which acts on
# them instead of displaying them.
HIDE_CURSOR = "\033[?25l"
ERASE_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"

# Physics and drawing constants, copied from the Java fields.
HEIGHT = 20.0
ROWS = 20
VELOCITY = 0.0
ACCELERATION = -0.1
FRAME_DELAY_SECONDS = 0.06


def draw_frame(height: float) -> None:
    """
    Render one frame, mirroring the inner loop of ``FallBall.main``.

    Java builds the frame with 20 ``println`` calls, printing ``O`` on the
    ball's row and a single space on every other row. Printing a space
    rather than nothing is what overwrites the previous ``O``; skipping the
    blank lines would leave a trail of old balls on screen.
    """
    # Move the cursor to the top-left corner before repainting.
    print(CURSOR_HOME, end="")
    # Java: int row = rows - (int) height. Height is measured from the
    # bottom, so subtract it from the row count to get a top-down row.
    row = ROWS - int(height)
    for y in range(1, ROWS + 1):
        if y == row:
            print("O")
        else:
            print(" ")


def main() -> None:
    """
    Mirror of ``FallBall.main``, including its ``while (true)`` loop.

    The loop ends by ``break`` when the ball reaches or passes the floor,
    not by the loop condition, exactly as in Java.
    """
    # Clear the screen and hide the cursor before the first frame.
    print(ERASE_SCREEN, end="")
    print(HIDE_CURSOR, end="")

    # ``height`` and ``velocity`` are local copies, because Python integers
    # and floats are immutable and Java's variables are updated in place.
    height = HEIGHT
    velocity = VELOCITY
    while True:
        # Euler integration: apply velocity to position, then gravity to
        # velocity. The order is significant and follows the Java lines.
        height = height + velocity
        velocity = velocity + ACCELERATION

        # Stop when the ball reaches the floor. Java's ``height <= 0`` is
        # the same comparison in Python.
        if height <= 0:
            break

        draw_frame(height)
        # 60 milliseconds. time.sleep takes seconds, hence the division.
        time.sleep(FRAME_DELAY_SECONDS)


if __name__ == "__main__":
    main()

