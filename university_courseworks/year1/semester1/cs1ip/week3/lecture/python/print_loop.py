"""
Line-by-line Python translation of ``week_03_lecture_code/PrintLoop.java``.

The Java program demonstrates how ``break`` leaves only the loop it is
written in. The outer loop runs i = 1, 2, 3 and the inner loop runs
j = 1, 2. When i = 2 and j = 2 the inner ``break`` fires, and the second
``break`` then leaves the outer loop as well.

Java to Python mapping used here:

  ``public class PrintLoop``          -> a plain module (no class needed)
  ``static void main(String[] args)`` -> ``def main() -> None``
  ``for (int i = 1; i <= 3; i++)``    -> ``for i in range(1, 4)``
  ``System.out.print``                -> ``print(..., end="")``
  ``System.out.println``              -> ``print(...)``

``range(1, 4)`` stops before 4, which is the same inclusive upper bound as
``i <= 3``. This off-by-one is the most common mistake when translating a
Java ``for`` loop: ``range(1, 3)`` would run only twice, not three times.
"""


def main() -> None:
    """
    Mirror of ``PrintLoop.main``.

    The output is three lines: i=1,j=1, then i=1,j=2, then i=2,j=1. The
    fourth pair (i=2, j=2) is never printed because the inner ``break``
    happens before the ``print`` call.
    """
    for i in range(1, 4):
        # Java declares ``int j`` before the loop so it stays visible after;
        # the initial value mirrors that even if the inner loop never runs.
        j = 0
        for j in range(1, 3):
            # Same guard as Java: stop the inner loop when both counters
            # reach 2. It runs before the print, so this pair is skipped.
            if i == 2 and j == 2:
                break
            # Java prints "i=" + i and then ",j=" + j on the same line.
            # One f-string replaces the two print calls.
            print(f"i={i},j={j}")
        # If the inner loop ended at j = 2 on the i = 2 pass, stop the
        # outer loop too; without this it would continue with i = 3.
        if i == 2 and j == 2:
            break


# The guard keeps the loop from running when the module is imported by a
# test or another program; only a direct ``python print_loop.py`` runs it.
if __name__ == "__main__":
    main()

