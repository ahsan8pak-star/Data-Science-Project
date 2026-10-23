"""
Line-by-line Python translation of ``week2/java/DCConvexHull.java``.

The Java program computes the convex hull of a set of 2D points in two
stages: a merge sort orders the points by x (then y), and a divide-and-conquer
lower-hull routine produces the boundary. A Swing window then draws every
input point in blue and the hull in green.

Java to Python mapping used here:

  ``LinkedList<T>``                       -> ``list[T]``
  ``addLast(x)`` / ``removeFirst()``      -> ``append(x)`` / ``pop(0)``
  ``peekFirst()`` / ``peekLast()``        -> ``xs[0]`` / ``xs[-1]``
  ``get(i)``                              -> ``xs[i]``
  ``Collections.sort(xs)``                -> ``xs.sort()``
  ``Comparable<Point>.compareTo``         -> ``Point.__lt__``
  ``toString()``                          -> ``__repr__``
  ``new LinkedList<T>(xs)``               -> ``list(xs)``
  ``Frame`` / ``paint(Graphics g)``       -> a ``tk.Tk`` window and a Canvas

``LinkedList`` is a doubly linked list, so ``removeFirst`` is constant time.
A Python ``list`` stores items contiguously, so ``pop(0)`` is linear in the
number of remaining items. The translation keeps ``pop(0)`` because it
preserves the Java algorithm exactly and the inputs here are tiny; a
``collections.deque`` would restore the constant-time removal but would lose
the fast indexing that the hull loops also need.

Java's ``Point == Point`` is reference identity because ``Point`` does not
override ``equals``. The equivalent Python test is ``is``, not ``==``, which
is why ``upper_lower_hull`` uses ``p is q`` for its duplicate check.
"""

import math
import random
import tkinter as tk


class Point:
    """
    Mirror of the Java ``Point`` class.

    Java declares ``x`` and ``y`` as public mutable fields. Python has no
    private fields either, so the same two attributes are used directly.
    """

    def __init__(self, x: float, y: float) -> None:
        """Mirror of ``Point(double x, double y)``."""
        self.x = x
        self.y = y

    def __lt__(self, other: "Point") -> bool:
        """
        Mirror of ``compareTo`` for use by ``list.sort``.

        Java compares x first and breaks ties with y. Python's ``sort`` only
        needs ``__lt__``; the tuple comparison below is the same order.
        ``(self.x, self.y) < (other.x, other.y)`` is written explicitly so
        the two coordinates stay visible.
        """
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def flip(self) -> None:
        """Mirror of ``flip``: negate y, reflecting the point in the x-axis."""
        self.y = self.y * -1

    def __repr__(self) -> str:
        """
        Mirror of ``toString``, including its missing space after the comma.

        The Java tests build expected strings such as ``[(1.0,5.0), ...]``,
        where the outer comma and space come from ``LinkedList.toString`` and
        the inner comma has none. Returning the same shape keeps those tests
        byte-for-byte identical.
        """
        return f"({self.x},{self.y})"


def split(xs: list) -> list:
    """
    Mirror of ``DCConvexHull.split``.

    Removes the first half of ``xs`` and returns it. ``xs`` is mutated in
    place and is left holding the second half. Java's ``removeFirst`` becomes
    ``pop(0)``.

    The mutation is the point of the function: ``merge_sort`` and
    ``lower_hull`` call it once and then pass each half to a separate
    recursive call. Copying instead of removing would make both calls see the
    same elements and recurse forever.
    """
    left = []
    half = len(xs) // 2
    for _ in range(half):
        left.append(xs.pop(0))
    return left


def merge(xs: list, ys: list) -> list:
    """
    Mirror of ``DCConvexHull.merge``.

    Merges two sorted lists into a new sorted list, emptying both inputs.
    ``<=`` on the comparison keeps equal elements in their original order,
    which is what makes the sort stable.
    """
    zs = []
    while xs and ys:
        # Java: xs.peekFirst().compareTo(ys.peekFirst()) <= 0
        # Python: ``not ys[0] < xs[0]`` sends ties down the left branch.
        if not ys[0] < xs[0]:
            zs.append(xs.pop(0))
        else:
            zs.append(ys.pop(0))

    # Drain whichever list still has items. Forgetting this leaves the tail
    # of one half out of the sorted result.
    while xs:
        zs.append(xs.pop(0))
    while ys:
        zs.append(ys.pop(0))
    return zs


def merge_sort(xs: list) -> list:
    """
    Mirror of ``DCConvexHull.merge_sort``.

    A list of zero or one item is already sorted. Otherwise the first half is
    split off, both halves are sorted recursively, and the results are
    merged. ``xs`` is emptied by ``split`` and ends up as the right half, so
    the second recursive call must use ``xs`` rather than the original data.
    """
    if xs is None or len(xs) <= 1:
        return xs
    left = split(xs)
    return merge(merge_sort(left), merge_sort(xs))


def cheat_sort(xs: list) -> list:
    """
    Mirror of ``DCConvexHull.cheat_sort``.

    A shortcut for the first task: copy the list and use the language's own
    sort instead of writing merge sort. ``list(xs)`` is the copy, matching
    ``new LinkedList<T>(xs)``, and ``sort`` uses ``Point.__lt__``.
    """
    ys = list(xs)
    ys.sort()
    return ys


def clockwise(p1: Point, p2: Point, p3: Point) -> bool:
    """
    Mirror of ``DCConvexHull.clockwise``.

    Returns true when the turn p1 -> p2 -> p3 is clockwise or the three points
    are collinear. The comparison uses gradients rearranged into a cross
    product, so no division by zero is possible when p1 and p2 share an
    x-coordinate.
    """
    return ((p3.y - p1.y) * (p2.x - p1.x)
            <= (p2.y - p1.y) * (p3.x - p1.x))


def _cross(o: Point, a: Point, b: Point) -> float:
    """
    Mirror of the private ``DCConvexHull.cross``.

    Positive means a counter-clockwise turn, negative a clockwise turn, and
    zero means the points are collinear. ``_cross`` uses a leading underscore
    to show that it is internal to the module, Python's convention where
    Java has ``private``.
    """
    return (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x)


def merge_disjoint_lower_hulls(left: list, right: list) -> list:
    """
    Mirror of ``DCConvexHull.merge_disjoint_lower_hulls``.

    Concatenates two lower hulls and removes the interior points with a
    stack. While the last two hull points and the new point make a clockwise
    or collinear turn, the middle point cannot be on the lower boundary and
    is popped.
    """
    if left is None or not left:
        return right
    if right is None or not right:
        return left

    ordered = []
    for p in left:
        ordered.append(p)
    for p in right:
        ordered.append(p)

    lower = []
    for p in ordered:
        # lower[-2], lower[-1] and p are the three points the turn test
        # needs. Java builds the same triple with get(size-2) and getLast().
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    return lower


def lower_hull(ps: list) -> list:
    """
    Mirror of ``DCConvexHull.lower_hull``.

    Zero, one or two points already form a lower hull, so they are returned
    as a copy. Larger inputs are split, each half's lower hull is computed,
    and the two disjoint chains are merged.
    """
    if ps is None or not ps or len(ps) <= 2:
        return list(ps)
    left = split(ps)
    left_hull = lower_hull(left)
    right_hull = lower_hull(ps)
    return merge_disjoint_lower_hulls(left_hull, right_hull)


def upper_lower_hull(ps: list) -> list:
    """
    Mirror of ``DCConvexHull.upper_lower_hull``.

    The lower hull is computed left to right. The upper hull is computed by
    scanning right to left with the same cross-product pruning, which is what
    makes the test remove points on the top chain rather than the bottom one.
    The two chains are then joined, skipping the endpoints they share.
    """
    if ps is None or not ps or len(ps) <= 2:
        return list(ps)

    # Copy before lower_hull, because split() consumes the list it is given.
    lower = lower_hull(list(ps))
    upper = []
    for i in range(len(ps) - 1, -1, -1):
        p = ps[i]
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    hull = []
    for p in lower:
        hull.append(p)
    for p in upper:
        # Java's p == q is identity, not value equality, because Point does
        # not override equals. Python's ``is`` is the same test.
        seen = False
        for q in hull:
            if p is q:
                seen = True
                break
        if not seen:
            hull.append(p)
    return hull


def merge_hull(ps: list) -> list:
    """
    Mirror of ``DCConvexHull.merge_hull``.

    Sorts the points first, then computes the hull. Sorting is essential: the
    divide step assumes increasing x so that the left and right halves are
    geometrically separate.
    """
    return upper_lower_hull(merge_sort(ps))


def line(ps: list[float]) -> list[Point]:
    """
    Mirror of ``DCConvexHull.line``.

    Converts a flat list of coordinates into a list of points. The Java loop
    advances by two, and the Python ``range`` does the same.
    """
    result = []
    for n in range(0, len(ps), 2):
        result.append(Point(ps[n], ps[n + 1]))
    return result


def test_merge() -> None:
    """
    Mirror of ``DCConvexHull.test_merge``.

    The five cases cover two empty lists, an empty right list, an empty left
    list, interleaved values and duplicates. A failure raises ``SystemExit``,
    which is the Python equivalent of Java's ``System.exit(-1)``.
    """
    xss = [[], [0], [], [1, 2, 3], [2, 4, 6, 8]]
    yss = [[], [], [1], [4, 5, 6], [1, 2, 3, 4]]
    outs = [
        "[]",
        "[0]",
        "[1]",
        "[1, 2, 3, 4, 5, 6]",
        "[1, 2, 2, 3, 4, 4, 6, 8]",
    ]
    for n, expect in enumerate(outs):
        xs = list(xss[n])
        ys = list(yss[n])
        print(f"Test: merge({xs}, {ys})")
        print(f"Expected: {expect}")
        actual = str(merge(xs, ys))
        if expect == actual:
            print("PASS\n")
        else:
            print(f"Actual: {actual}")
            print("FAIL")
            raise SystemExit(-1)


def test_merge_sort() -> None:
    """Mirror of ``DCConvexHull.test_merge_sort``, with the same six cases."""
    xss = [[], [0], [1, 2], [2, 1], [2, 7, 5, 1, 6, 8, 3, 4], [3, 1, 4, 5, 6, 2, 7]]
    outs = [
        "[]",
        "[0]",
        "[1, 2]",
        "[1, 2]",
        "[1, 2, 3, 4, 5, 6, 7, 8]",
        "[1, 2, 3, 4, 5, 6, 7]",
    ]
    for n, expect in enumerate(outs):
        xs = list(xss[n])
        print(f"Test: merge_sort({xs})")
        print(f"Expected: {expect}")
        actual = str(merge_sort(xs))
        if expect == actual:
            print("PASS\n")
        else:
            print(f"Actual: {actual}")
            print("FAIL")
            raise SystemExit(-1)


def test_merge_disjoint_lower_hulls() -> None:
    """
    Mirror of ``DCConvexHull.test_merge_disjoint_lower_hulls``.

    Each case supplies a left hull, a right hull and the expected combined
    chain. The expected strings rely on ``Point.__repr__`` having no space
    after the inner comma.
    """
    lefts = [
        [1.0, 5.0, 2.0, 1.0],
        [1.0, 5.0, 2.0, 1.0, 3.0, 5.0],
        [1.0, 5.0, 2.0, 6.0, 3.0, 7.0, 4.0, 8.0],
        [1.0, 5.0, 2.0, 0.0],
    ]
    rights = [
        [4.0, 1.0, 5.0, 5.0],
        [4.0, 5.0, 5.0, 1.0, 6.0, 5.0],
        [5.0, 1.0, 6.0, 1.0],
        [3.0, 5.0, 4.0, 4.5, 5.0, 4.0, 6.0, 3.5],
    ]
    outs = [
        "[(1.0,5.0), (2.0,1.0), (4.0,1.0), (5.0,5.0)]",
        "[(1.0,5.0), (2.0,1.0), (5.0,1.0), (6.0,5.0)]",
        "[(1.0,5.0), (5.0,1.0), (6.0,1.0)]",
        "[(1.0,5.0), (2.0,0.0), (6.0,3.5)]",
    ]
    for n, expect in enumerate(outs):
        left = line(lefts[n])
        right = line(rights[n])
        print(f"Test: merge_disjoint_lower_hulls({left}, {right})")
        print(f"Expected: {expect}")
        actual = str(merge_disjoint_lower_hulls(left, right))
        if expect == actual:
            print("PASS\n")
        else:
            print(f"Actual: {actual}")
            print("FAIL")
            raise SystemExit(-1)


class ConvexHullPlot:
    """
    Mirror of the Java ``ConvexHullPlot`` class.

    Java subclasses ``Frame`` and overrides ``paint``. This version owns a
    tkinter root window and Canvas, and ``paint`` receives the Canvas. The
    y-axis is still flipped with ``500 - y`` because screen coordinates run
    downward while the algorithm's coordinates run upward.
    """

    def __init__(self, all_points: list[Point], hull: list[Point]) -> None:
        """Mirror of the ``ConvexHullPlot`` constructor."""
        self.all = all_points
        self.hull = hull

        self.root = tk.Tk()
        self.root.title("Convex Hull")
        self.root.geometry("500x500")
        # Java's windowClosing listener disposes the frame; closing a Tk
        # window destroys it by default, so no extra listener is needed.
        self.canvas = tk.Canvas(
            self.root, width=500, height=500,
            background="white", highlightthickness=0,
        )
        self.canvas.pack()
        self.paint(self.canvas)

    def paint(self, canvas: tk.Canvas) -> None:
        """
        Mirror of ``ConvexHullPlot.paint``.

        All points are drawn first in blue, then the hull perimeter in green.
        Drawing the points first means the green lines sit on top of them.
        """
        canvas.delete("all")  # super.paint(g)

        # g.setColor(Color.BLUE); g.fillOval((int) p.x, 500 - (int) p.y, 5, 5)
        for p in self.all:
            x = int(p.x)
            y = 500 - int(p.y)
            canvas.create_oval(x, y, x + 5, y + 5, fill="blue", outline="blue")

        # g.setColor(Color.GREEN); Point p1 = hull.peekLast();
        # The last point starts the closing edge, so the loop ends where it began.
        canvas_colour = "green"
        p1 = self.hull[-1]
        for p2 in self.hull:
            canvas.create_line(
                int(p1.x), 500 - int(p1.y),
                int(p2.x), 500 - int(p2.y),
                fill=canvas_colour,
            )
            p1 = p2

    def show(self) -> None:
        """Mirror of ``setVisible(true)`` plus Swing's event loop."""
        self.root.mainloop()


def main() -> None:
    """
    Mirror of ``DCConvexHull.main``.

    Runs the three test groups, then builds an inner ring of random points
    and an outer ring of fixed points. ``all_points`` is copied before
    ``merge_hull`` because the merge sort consumes the input list.
    """
    test_merge()
    print("Testing Task 1.1 complete.\n")
    test_merge_sort()
    print("Testing Task 1.2 complete.\n")
    test_merge_disjoint_lower_hulls()
    print("Testing Task 2.1 complete.\n")

    rng = random.Random()
    ps: list[Point] = []

    # Java's r.nextDouble() returns [0.0, 1.0); Python's random() matches.
    for n in range(40):
        theta = (2.0 * math.pi / 10.0) * (n + rng.random())
        radius = 125.0 * (0.5 + rng.random())
        x = 250.0 + (radius * math.cos(theta))
        y = 250.0 + (radius * math.sin(theta))
        ps.append(Point(x, y))

    for n in range(10):
        theta = (2.0 * math.pi / 10.0) * n
        radius = 200.0
        x = 250.0 + (radius * math.cos(theta))
        y = 250.0 + (radius * math.sin(theta))
        ps.append(Point(x, y))

    all_points = list(ps)
    hull = merge_hull(ps)
    ConvexHullPlot(all_points, hull).show()


if __name__ == "__main__":
    # The Java program has no headless mode: importing this module would
    # open a window, so the work only runs when the file is executed.
    main()

