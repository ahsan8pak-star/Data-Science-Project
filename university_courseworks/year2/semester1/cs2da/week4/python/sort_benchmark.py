"""
Line-by-line Python translation of ``week4/java/SortBenchmark.java``.

The Java program times four sorting algorithms on random integer arrays and
prints CSV rows of ``algorithm,input-size,milliseconds``. Each algorithm is a
separate helper class in the original, and the translation keeps that shape.

Java to Python mapping used here:

  ``ThreadMXBean.getCurrentThreadCpuTime()`` -> ``time.thread_time_ns()``
  ``private static long time``                -> a module-level ``_timer_start``
  ``Random.nextInt()``                        -> ``randint(-2**31, 2**31 - 1)``
  ``Comparable[].compareTo``                  -> the ``<`` and ``>`` operators
  ``System.out.printf("%n")``                 -> ``print`` with an f-string
  ``Integer[]``                               -> ``list[int]``

``time.thread_time_ns`` is the closest Python equivalent of
``getCurrentThreadCpuTime``: both measure CPU time consumed by the current
thread, in nanoseconds, and both exclude time spent sleeping. It is not the
same as ``perf_counter_ns`` (wall-clock time) or ``process_time_ns`` (all
threads), and using either of those would change what the benchmark measures.

Java's ``int`` is 32 bits wide, so ``nextInt()`` covers -2^31 to 2^31 - 1.
Python integers are unbounded, so the range is written out explicitly to
produce inputs of the same size. A plain ``randint(0, n)`` would not.
"""

import random
import time

# Java: private static long time = -1; a module-level name plays the role of
# the static field, and the leading underscore marks it as internal.
_timer_start = -1

# Java: private static Random r = null;
_rng: random.Random | None = None

# 10 seconds, written in nanoseconds because stop_timer returns nanoseconds.
TIME_LIMIT_NANOSECONDS = 10_000_000_000
NANOSECONDS_PER_MILLISECOND = 1_000_000

# Java's int range, used to keep the random inputs the same size.
JAVA_INT_MIN = -(2 ** 31)
JAVA_INT_MAX = 2 ** 31 - 1


def start_timer() -> None:
    """
    Mirror of ``SortBenchmark.start_timer``.

    Java throws ``Error`` if a timer is already running. Python has no
    ``Error`` class, so ``RuntimeError`` is used for the same programming
    mistake. ``global`` is required because the assignment rebinds the
    module-level name rather than creating a local one.
    """
    global _timer_start
    if _timer_start == -1:
        _timer_start = time.thread_time_ns()
    else:
        raise RuntimeError("timer already started")


def stop_timer() -> int:
    """
    Mirror of ``SortBenchmark.stop_timer``.

    Returns the elapsed CPU time in nanoseconds and resets the timer so the
    next ``start_timer`` works. Calling it without a start is an error in
    both languages.
    """
    global _timer_start
    if _timer_start == -1:
        raise RuntimeError("timer was not started")
    difference = time.thread_time_ns() - _timer_start
    _timer_start = -1
    return difference


def random_list(n: int) -> list[int]:
    """
    Mirror of ``SortBenchmark.random_list``.

    The caller reseeds ``_rng`` before each algorithm so that all four sorts
    receive the same input. Without the reseeding the timings would compare
    different data, which is the mistake the Java comments warn about.
    """
    a = [0] * n
    for x in range(n):
        a[x] = _rng.randint(JAVA_INT_MIN, JAVA_INT_MAX)
    return a


def print_array(a: list) -> None:
    """
    Mirror of ``SortBenchmark.print_array``.

    Java prints every element followed by a space and then a newline, so the
    line ends with a trailing space. The two ``print`` calls reproduce that
    exactly; ``" ".join`` would not, because it omits the final space.
    """
    for x in a:
        print(x, end=" ")
    print()


class Insertion:
    """
    Mirror of the Java ``Insertion`` class.

    Java gives the class a private constructor to stop callers creating
    instances. Python has no enforced private constructor; the convention is
    to leave the class without instance state and call the static methods
    through the class name.
    """

    @staticmethod
    def sort(a: list) -> None:
        """Mirror of ``Insertion.sort``: insertion sort in ascending order."""
        n = len(a)
        for i in range(1, n):
            # j walks left while the item before it is larger. The condition
            # is checked before each exchange, so j can reach zero safely.
            j = i
            while j > 0 and a[j] < a[j - 1]:
                a[j], a[j - 1] = a[j - 1], a[j]
                j -= 1

    @staticmethod
    def _less(v, w) -> bool:
        """Mirror of ``Insertion.less``: Java's ``compareTo(w) < 0``."""
        return v < w

    @staticmethod
    def _exchange(a: list, i: int, j: int) -> None:
        """Mirror of ``Insertion.exch``, using Python's tuple swap."""
        a[i], a[j] = a[j], a[i]


class MergeBU:
    """
    Mirror of the Java ``MergeBU`` class: bottom-up merge sort.

    The iterative form avoids recursion. ``len`` doubles on each pass, and
    each pass merges adjacent blocks of that length.
    """

    @staticmethod
    def _merge(a: list, aux: list, lo: int, mid: int, hi: int) -> None:
        """
        Mirror of ``MergeBU.merge``: stably merge a[lo..mid] with a[mid+1..hi].

        ``aux`` is reused between calls rather than allocated per merge. The
        copy into ``aux`` is what allows the merge to write back into ``a``
        without overwriting values it has not read yet.
        """
        for k in range(lo, hi + 1):
            aux[k] = a[k]

        i = lo
        j = mid + 1
        for k in range(lo, hi + 1):
            if i > mid:
                a[k] = aux[j]
                j += 1
            elif j > hi:
                a[k] = aux[i]
                i += 1
            elif aux[j] < aux[i]:
                a[k] = aux[j]
                j += 1
            else:
                # The else branch takes aux[i] on ties, which is what keeps
                # the merge stable.
                a[k] = aux[i]
                i += 1

    @staticmethod
    def sort(a: list) -> None:
        """Mirror of ``MergeBU.sort``: merge blocks of doubling width."""
        n = len(a)
        aux = [None] * n
        length = 1
        while length < n:
            lo = 0
            while lo < n - length:
                mid = lo + length - 1
                hi = min(lo + length + length - 1, n - 1)
                MergeBU._merge(a, aux, lo, mid, hi)
                lo += length + length
            length *= 2

    @staticmethod
    def _less(v, w) -> bool:
        """Mirror of ``MergeBU.less``."""
        return v < w


class Quick3way:
    """
    Mirror of the Java ``Quick3way`` class: quicksort with 3-way partitioning.

    The array is shuffled first so that an already-sorted input cannot
    trigger the O(n^2) worst case. The three-way partition then groups values
    less than, equal to and greater than the pivot.
    """

    @staticmethod
    def sort(a: list) -> None:
        """Mirror of ``Quick3way.sort``: shuffle, then sort the whole array."""
        Quick3way.shuffle(a)
        Quick3way._sort(a, 0, len(a) - 1)

    @staticmethod
    def shuffle(a: list) -> None:
        """
        Mirror of ``Quick3way.shuffle``.

        Java uses ``Math.random()``, which is a separate generator from the
        seeded ``Random r`` used for the inputs. Python's module-level
        ``random.random()`` has the same role: it is not reseeded by
        ``Random(20241024)``, so the shuffle stays independent of the input
        generator, as in the Java program.
        """
        n = len(a)
        for i in range(n):
            # Index uniformly in [0, i]. int() truncates, as in Java.
            r = int(random.random() * (i + 1))
            a[r], a[i] = a[i], a[r]

    @staticmethod
    def _sort(a: list, lo: int, hi: int) -> None:
        """
        Mirror of the private ``Quick3way.sort``.

        ``lt`` marks the end of the smaller-than-pivot region and ``gt`` the
        start of the larger-than-pivot region. Everything between them
        equals the pivot, so those elements never need to move again.
        """
        if hi <= lo:
            return

        lt = lo
        gt = hi
        v = a[lo]
        i = lo + 1

        while i <= gt:
            if a[i] < v:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > v:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1

        # Recursively sort the two outer regions. The equal region is done.
        Quick3way._sort(a, lo, lt - 1)
        Quick3way._sort(a, gt + 1, hi)

    @staticmethod
    def _less(v, w) -> bool:
        """Mirror of ``Quick3way.less``."""
        return v < w

    @staticmethod
    def _exchange(a: list, i: int, j: int) -> None:
        """Mirror of ``Quick3way.exch``."""
        a[i], a[j] = a[j], a[i]


class Shell:
    """
    Mirror of the Java ``Shell`` class: Shell sort with the 3x+1 sequence.

    The stride sequence is 1, 4, 13, 40, ... Each pass h-sorts the array,
    and the final pass with h = 1 is an insertion sort over a nearly sorted
    array, which is why it is fast.
    """

    @staticmethod
    def sort(a: list) -> None:
        """Mirror of ``Shell.sort``."""
        n = len(a)

        h = 1
        while h < n // 3:
            h = 3 * h + 1

        while h >= 1:
            for i in range(h, n):
                j = i
                while j >= h and a[j] < a[j - h]:
                    a[j], a[j - h] = a[j - h], a[j]
                    j -= h
            # Java's h /= 3 on an int truncates; Python's // does the same.
            h //= 3

    @staticmethod
    def _less(v, w) -> bool:
        """Mirror of ``Shell.less``."""
        return v < w

    @staticmethod
    def _exchange(a: list, i: int, j: int) -> None:
        """Mirror of ``Shell.exch``."""
        a[i], a[j] = a[j], a[i]


def main() -> None:
    """
    Mirror of ``SortBenchmark.main``.

    Runs the four benchmark tasks in the Java order. Each task reseeds the
    generator with 20241024, so every algorithm starts from identical input.
    The loop condition is checked before each run, and ``n`` grows by twenty
    percent after each run, in the same order as the Java ``for`` update.
    """
    global _timer_start, _rng
    _timer_start = -1

    # TASK: INSERTION SORT
    _rng = random.Random(20241024)
    elapsed_nanoseconds = 0
    n = 10000
    while elapsed_nanoseconds < TIME_LIMIT_NANOSECONDS:
        a = random_list(n)
        start_timer()
        Insertion.sort(a)
        elapsed_nanoseconds = stop_timer()
        milliseconds = elapsed_nanoseconds // NANOSECONDS_PER_MILLISECOND
        print(f"insertion,{n},{milliseconds}")
        n = (n * 12) // 10

    # TASK: MERGE SORT
    _rng = random.Random(20241024)
    elapsed_nanoseconds = 0
    n = 10000
    while elapsed_nanoseconds < TIME_LIMIT_NANOSECONDS:
        a = random_list(n)
        start_timer()
        MergeBU.sort(a)
        elapsed_nanoseconds = stop_timer()
        milliseconds = elapsed_nanoseconds // NANOSECONDS_PER_MILLISECOND
        print(f"merge,{n},{milliseconds}")
        n = (n * 12) // 10

    # TASK: QUICKSORT (3-WAY)
    _rng = random.Random(20241024)
    elapsed_nanoseconds = 0
    n = 10000
    while elapsed_nanoseconds < TIME_LIMIT_NANOSECONDS:
        a = random_list(n)
        start_timer()
        Quick3way.sort(a)
        elapsed_nanoseconds = stop_timer()
        milliseconds = elapsed_nanoseconds // NANOSECONDS_PER_MILLISECOND
        print(f"quick,{n},{milliseconds}")
        n = (n * 12) // 10

    # TASK: SHELL SORT
    _rng = random.Random(20241024)
    elapsed_nanoseconds = 0
    n = 10000
    while elapsed_nanoseconds < TIME_LIMIT_NANOSECONDS:
        a = random_list(n)
        start_timer()
        Shell.sort(a)
        elapsed_nanoseconds = stop_timer()
        milliseconds = elapsed_nanoseconds // NANOSECONDS_PER_MILLISECOND
        print(f"shell,{n},{milliseconds}")
        n = (n * 12) // 10


if __name__ == "__main__":
    # The Java program runs for at least 40 seconds (four loops, each until
    # one sort exceeds ten seconds), so it only runs when asked for.
    main()

