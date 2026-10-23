"""
Line-by-line Python translation of ``week_03_lecture_code/BounceBall.java``.

This extends ``FallBall`` with a floor: when the ball reaches height zero it
keeps its position for one frame, reverses its velocity, and loses energy
on each bounce. The animation stops once the rebound speed is 0.5 or less.

Java to Python mapping used here:

  ``velocity = velocity * -1.0 * elasticity`` -> the same arithmetic is valid
  ``if (height <= 0.0) { ... } else { ... }`` -> ``if`` / ``else`` unchanged
  ``Thread.sleep(60)``                        -> ``time.sleep(0.06)``
  ``break`` inside the loop                   -> ``break`` inside the loop

Watch the difference between ``BounceBall`` and ``FallBall``: ``FallBall``
applies acceleration every frame and stops on impact, while ``BounceBall``
only applies acceleration while the ball is in the air. Applying gravity on
the bounce frame would pull the ball through the floor, which is the usual
translation mistake here.
"""

import time

# ANSI control sequences, identical to the Java string constants.
HIDE_CURSOR = "\033[?25l"
ERASE_SCREEN = "\033[2J"
CURSOR_HOME = "\033[H"

HEIGHT = 20.0
ROWS = 20
VELOCITY = 0.0
ACCELERATION = -0.1
ELASTICITY = 0.6
FRAME_DELAY_SECONDS = 0.06

# The ball stops once its rebound speed falls to this value or below.
MINIMUM_BOUNCE_SPEED = 0.5


def draw_frame(height: float) -> None:
    """
    Render one frame, mirroring the inner loop of ``BounceBall.main``.

    The row calculation is the same as ``FallBall.draw_frame``. It is
    repeated rather than imported so that each file stands alone as the
    translation of its own Java file, which is what makes them readable
    side by side.
    """
    print(CURSOR_HOME, end="")
    row = ROWS - int(height)
    for y in range(1, ROWS + 1):
        if y == row:
            print("O")
        else:
            print(" ")


def main() -> None:
    """
    Mirror of ``BounceBall.main``.

    The height update happens first in both languages, so the ball reaches
    the floor one frame before the bounce is handled. Java then restores the
    pre-impact height with ``height = height - velocity`` (velocity is
    negative, so this adds the distance back), which is reproduced below.
    """
    print(ERASE_SCREEN, end="")
    print(HIDE_CURSOR, end="")

    height = HEIGHT
    velocity = VELOCITY
    while True:
        # Move first. The Java code does not apply gravity before this
        # line; it only applies it in the ``else`` branch below.
        height = height + velocity

        if height <= 0.0:
            # Undo the last movement so the ball sits on the floor for this
            # frame instead of disappearing below it.
            height = height - velocity
            # Reverse and damp the velocity. Multiplying by -1.0 flips the
            # direction; ELASTICITY removes energy on every bounce.
            velocity = velocity * -1.0 * ELASTICITY
            if velocity <= MINIMUM_BOUNCE_SPEED:
                break
        else:
            # Gravity only acts while the ball is above the floor.
            velocity = velocity + ACCELERATION

        draw_frame(height)
        time.sleep(FRAME_DELAY_SECONDS)


if __name__ == "__main__":
    main()

