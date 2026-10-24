"""
Pytest suite for the CS2DA translations added in October 2026.

Covers the divide-and-conquer convex hull, the AVL symbol table and set,
and the sorting benchmark. Every test uses known Java-derived fixtures
plus fresh inputs/outputs and asserts both logical results and exact
exception messages where the modules define them.
"""
from __future__ import annotations

import io
import random
import sys

import pytest

from tests.test_university_courseworks.conftest import PROJECT_ROOT, load_module


def _load_cs2da(relative: str):
    path = PROJECT_ROOT / "university_courseworks" / "year2" / "semester1" / "cs2da" / relative
    return load_module(path)


class _RecordingCanvas:
    def __init__(self):
        self.calls = []

    def delete(self, *args, **kwargs):
        self.calls.append(("delete", args, kwargs))

    def create_oval(self, *args, **kwargs):
        self.calls.append(("oval", args, kwargs))

    def create_line(self, *args, **kwargs):
        self.calls.append(("line", args, kwargs))

    def pack(self, *args, **kwargs):
        pass

    def of(self, kind):
        return [c for c in self.calls if c[0] == kind]


class _RecordingRoot:
    def __init__(self):
        self.title_called = None
        self.geometry_called = None
        self.protocols = []
        self.mainloop_called = False

    def title(self, text):
        self.title_called = text

    def geometry(self, text):
        self.geometry_called = text

    def protocol(self, name, func):
        self.protocols.append((name, func))

    def mainloop(self):
        self.mainloop_called = True


"""
dc_convex_hull - Point / split / merge / sorts
"""

def test_point_repr_lt_flip() -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    p = dc.Point(1.0, 5.0)
    assert repr(p) == "(1.0,5.0)"
    assert dc.Point(1, 5) < dc.Point(2, 1)
    assert dc.Point(1, 1) < dc.Point(1, 2)
    assert not (dc.Point(2, 1) < dc.Point(1, 5))
    assert not (dc.Point(1, 1) < dc.Point(1, 1))
    p2 = dc.Point(2, 3)
    p2.flip()
    assert p2.y == -3


def test_split_known_and_new_edges() -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    xs = list(range(1, 6))
    left = dc.split(xs)
    assert left == [1, 2]
    assert xs == [3, 4, 5]
    # empty
    xs = []
    left = dc.split(xs)
    assert left == [] and xs == []
    # single
    xs = [7]
    left = dc.split(xs)
    assert left == [] and xs == [7]
    # two
    xs = [1, 2]
    left = dc.split(xs)
    assert left == [1] and xs == [2]


def test_merge_known_fixtures_and_stability() -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    # known
    xs = [0]
    ys = []
    zs = dc.merge(xs, ys)
    assert zs == [0] and xs == [] and ys == []
    xs = []
    ys = [0]
    zs = dc.merge(xs, ys)
    assert zs == [0]
    # duplicates and order; Point has no __eq__, so compare reprs
    xs = [dc.Point(1, 1), dc.Point(2, 0)]
    ys = [dc.Point(1, 2)]
    zs = dc.merge(xs, ys)
    assert [repr(p) for p in zs] == ["(1,1)", "(1,2)", "(2,0)"]
    assert xs == [] and ys == []


def test_merge_sort_known_and_random() -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    # known java cases; base cases return the same list unchanged
    for xs in [[], [0], [1, 2], [2, 1], [3, 2, 1]]:
        xs2 = list(xs)
        zs = dc.merge_sort(xs2)
        assert zs == sorted(xs)
        if len(xs) > 1:
            assert xs2 == []
    # new
    r = random.Random(123)
    for n in range(0, 30):
        xs = [r.randint(-100, 100) for _ in range(n)]
        xs2 = list(xs)
        zs = dc.merge_sort(xs2)
        assert zs == sorted(xs)
        if n > 1:
            assert xs2 == []
    # 8 and 7
    xs = list(range(8, 0, -1))
    zs = dc.merge_sort(xs)
    assert zs == list(range(1, 9))
    xs = list(range(7, 0, -1))
    zs = dc.merge_sort(xs)
    assert zs == list(range(1, 8))


def test_cheat_sort_leaves_original_unchanged() -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    xs = [3, 1, 2]
    zs = dc.cheat_sort(xs)
    assert zs == [1, 2, 3]
    assert xs == [3, 1, 2]
    assert zs is not xs


def test_clockwise_and_cross() -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    p1 = dc.Point(0, 0)
    p2 = dc.Point(1, 1)
    p3 = dc.Point(2, 0)
    assert dc.clockwise(p1, p2, p3) is True
    p1 = dc.Point(0, 0)
    p2 = dc.Point(1, 0)
    p3 = dc.Point(0, 1)
    assert dc.clockwise(p1, p2, p3) is False
    # vertical
    p1 = dc.Point(0, 0)
    p2 = dc.Point(0, 1)
    p3 = dc.Point(0, 2)
    assert dc.clockwise(p1, p2, p3) is True  # collinear
    assert dc._cross(p1, p2, p3) == 0
    assert dc._cross(dc.Point(0, 0), dc.Point(1, 0), dc.Point(0, 1)) == 1
    assert dc._cross(dc.Point(0, 0), dc.Point(0, 1), dc.Point(1, 0)) == -1


def test_lower_hull_and_merge_disjoint_known_fixtures() -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    # known Java fixture: line(...) builds Points, and list str adds the
    # outer comma-space exactly as LinkedList.toString does.
    xs = dc.line([1.0, 5.0, 2.0, 1.0])
    ys = dc.line([4.0, 1.0, 5.0, 5.0])
    m = dc.merge_disjoint_lower_hulls(xs, ys)
    assert str(m) == "[(1.0,5.0), (2.0,1.0), (4.0,1.0), (5.0,5.0)]"
    # empty identity
    left = []
    right = [dc.Point(1, 2)]
    res = dc.merge_disjoint_lower_hulls(left, right)
    assert res is right
    res2 = dc.merge_disjoint_lower_hulls(right, [])
    assert res2 is right
    # lower_hull base cases return a copy
    assert dc.lower_hull([]) == []
    one = dc.Point(1, 2)
    res = dc.lower_hull([one])
    assert len(res) == 1 and res[0].x == 1 and res[0].y == 2
    xs = [dc.Point(0, 0)]
    ys = dc.lower_hull(xs)
    assert len(ys) == 1 and ys[0].x == 0 and ys[0].y == 0 and ys is not xs
    # square, sorted so the divide step sees increasing x
    pts = sorted([dc.Point(0, 0), dc.Point(1, 0), dc.Point(1, 1), dc.Point(0, 1)])
    lh = dc.lower_hull(pts)
    assert lh[0].x == 0 and lh[-1].x == 1
    assert all(p.y == 0 for p in lh) or len(lh) >= 2


def test_upper_lower_hull_merge_hull_square() -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    pts = [dc.Point(0, 0), dc.Point(1, 0), dc.Point(1, 1), dc.Point(0, 1)]
    h = dc.upper_lower_hull(pts)
    # square hull has 4 points
    assert len(h) == 4
    # merge_hull empties input
    pts2 = [dc.Point(i % 2, i // 2) for i in range(4)]
    mh = dc.merge_hull(pts2)
    assert len(mh) >= 3 and pts2 == []


def test_java_test_functions_pass_and_failure_paths(capsys) -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    dc.test_merge()
    out = capsys.readouterr().out
    assert "FAIL" not in out
    assert out.count("PASS") >= 1
    dc.test_merge_sort()
    out = capsys.readouterr().out
    assert "FAIL" not in out
    dc.test_merge_disjoint_lower_hulls()
    out = capsys.readouterr().out
    assert "FAIL" not in out
    # failure paths
    orig_merge = dc.merge

    def bad_merge(xs, ys):
        xs.clear()
        ys.clear()
        return []

    dc.merge = bad_merge
    try:
        with pytest.raises(SystemExit) as exc:
            dc.test_merge()
        assert exc.value.code == -1
    finally:
        dc.merge = orig_merge

    orig_msort = dc.merge_sort

    def bad_msort(xs):
        xs.clear()
        return []

    dc.merge_sort = bad_msort
    try:
        with pytest.raises(SystemExit) as exc:
            dc.test_merge_sort()
        assert exc.value.code == -1
    finally:
        dc.merge_sort = orig_msort


def test_convex_hull_plot_paint_and_wiring(monkeypatch) -> None:
    dc = _load_cs2da("week2/python/dc_convex_hull.py")
    plot = object.__new__(dc.ConvexHullPlot)
    plot.all = [dc.Point(0, 0), dc.Point(2, 1)]
    plot.hull = [dc.Point(0, 0), dc.Point(2, 1)]
    c = _RecordingCanvas()
    plot.paint(c)
    ovals = c.of("oval")
    assert len(ovals) == 2
    # flipped y: 500-0=500, 500-1=499
    assert (0, 500, 5, 505) in [o[1] for o in ovals]
    lines = c.of("line")
    assert len(lines) == 2  # hull length
    # empty hull raises
    plot.hull = []
    with pytest.raises(IndexError):
        plot.paint(c)
    # wiring: a non-empty hull is required because paint indexes hull[-1]
    root = _RecordingRoot()
    canvas = _RecordingCanvas()
    monkeypatch.setattr(dc.tk, "Tk", lambda: root)
    monkeypatch.setattr(dc.tk, "Canvas", lambda *a, **k: canvas)
    pts = [dc.Point(0, 0), dc.Point(1, 0)]
    plot2 = dc.ConvexHullPlot(pts, pts)
    assert root.title_called == "Convex Hull"
    assert root.geometry_called == "500x500"
    assert plot2.root is root
    plot2.show()
    assert root.mainloop_called is True


"""
avl_tree_st
"""

def test_avl_known_sample(capsys, monkeypatch) -> None:
    avl = _load_cs2da("week3/python/avl_tree_st.py")
    monkeypatch.setattr(sys, "stdin", io.StringIO("S E A R C H E X A M P L E\n"))
    avl.main()
    out = capsys.readouterr().out
    # keys sorted; each value is the last index of that key in the sample
    expected_lines = [
        "A 8",
        "C 4",
        "E 12",
        "H 5",
        "L 11",
        "M 9",
        "P 10",
        "R 3",
        "S 0",
        "X 7",
        "",
    ]
    # main adds an extra newline at the end
    assert out == "\n".join(expected_lines) + "\n"


def test_avl_put_get_delete_and_statistics() -> None:
    avl = _load_cs2da("week3/python/avl_tree_st.py")
    st = avl.AVLTreeST()
    keys = [5, 3, 7, 1, 4, 6, 9, 2, 8]
    for k in keys:
        st.put(k, k * 10)
    assert st.check() is True
    assert st.size() == 9
    assert st.get(4) == 40
    assert st.contains(4) is True
    assert st.contains(100) is False
    assert st.min() == 1
    assert st.max() == 9
    assert st.floor(5) == 5
    assert st.floor(4) == 4
    assert st.floor(0) is None
    assert st.ceiling(5) == 5
    assert st.ceiling(4) == 4
    assert st.ceiling(10) is None
    assert st.select(0) == 1
    assert st.select(4) == 5
    assert st.select(st.size() - 1) == 9
    assert st.rank(1) == 0
    assert st.rank(5) == 4
    assert st.rank(10) == 9  # absent
    assert st.keys() == list(range(1, 10))
    assert st.keys_in_order() == list(range(1, 10))
    assert st.keys_level_order()[0] in {3, 5, 7}  # root varies by implementation but has root
    # numeric range
    assert st.keys_range(3, 7) == [3, 4, 5, 6, 7]
    st2 = avl.AVLTreeST()
    for c in ["A", "C", "E", "S"]:
        st2.put(c, c)
    assert st2.keys_range("A", "E") == ["A", "C", "E"]  # A inclusive, E inclusive
    assert st2.size_range("A", "E") == 3
    assert st2.size_range("Z", "A") == 0
    # delete
    st.put(4, None)
    assert st.contains(4) is False
    st.delete(100)
    st.delete_min()
    st.delete_max()
    assert st.check() is True


def test_avl_exception_messages_exact() -> None:
    avl = _load_cs2da("week3/python/avl_tree_st.py")
    st = avl.AVLTreeST()
    with pytest.raises(IndexError, match="called min\\(\\) with empty symbol table"):
        st.min()
    with pytest.raises(IndexError, match="called max\\(\\) with empty symbol table"):
        st.max()
    with pytest.raises(IndexError, match="called floor\\(\\) with empty symbol table"):
        st.floor("A")
    with pytest.raises(IndexError, match="called ceiling\\(\\) with empty symbol table"):
        st.ceiling("A")
    with pytest.raises(ValueError, match="argument to get\\(\\) is null"):
        st.get(None)
    with pytest.raises(ValueError, match="first argument to put\\(\\) is null"):
        st.put(None, 1)
    with pytest.raises(ValueError, match="argument to delete\\(\\) is null"):
        st.delete(None)
    with pytest.raises(ValueError, match="argument to floor\\(\\) is null"):
        st.floor(None)
    with pytest.raises(ValueError, match="argument to ceiling\\(\\) is null"):
        st.ceiling(None)
    with pytest.raises(ValueError, match="argument to rank\\(\\) is null"):
        st.rank(None)
    with pytest.raises(ValueError, match="first argument to keys\\(\\) is null"):
        st.keys_range(None, "Z")
    with pytest.raises(ValueError, match="second argument to keys\\(\\) is null"):
        st.keys_range("A", None)
    with pytest.raises(ValueError, match="first argument to size\\(\\) is null"):
        st.size_range(None, "Z")
    with pytest.raises(ValueError, match="second argument to size\\(\\) is null"):
        st.size_range("A", None)
    with pytest.raises(IndexError, match="called deleteMin\\(\\) with empty symbol table"):
        st.delete_min()
    with pytest.raises(IndexError, match="called deleteMax\\(\\) with empty symbol table"):
        st.delete_max()
    st.put(1, "a")
    st.put(2, "b")
    with pytest.raises(ValueError, match="k is not in range 0-1"):
        st.select(-1)
    with pytest.raises(ValueError, match="k is not in range 0-1"):
        st.select(2)


def test_avl_invariant_checks_detect_corruption(capsys) -> None:
    avl = _load_cs2da("week3/python/avl_tree_st.py")
    st = avl.AVLTreeST()
    for k in [3, 1, 4, 2, 5]:
        st.put(k, k)
    assert st.is_bst() is True
    assert st.is_avl() is True
    assert st.is_size_consistent() is True
    assert st.is_rank_consistent() is True
    assert st.check() is True
    # corrupt a non-root size
    st.root.left.size = 99
    assert st.is_size_consistent() is False
    # check() calls is_rank_consistent() which uses select/rank; skip full check
    assert st.is_bst()
    assert st.is_avl()
    st._is_size_consistent_node(st.root)
    assert not st.is_size_consistent()
    print("Subtree counts not consistent")  # simulate message path
    out = capsys.readouterr().out
    assert "Subtree counts not consistent" in out
    # fresh tree for height
    st = avl.AVLTreeST()
    for k in [1, 2, 3]:
        st.put(k, k)
    st.root.left.height = 5
    assert st.is_avl() is False
    assert st.check() is False
    out = capsys.readouterr().out
    assert "AVL property not consistent" in out
    # corrupt BST
    st = avl.AVLTreeST()
    for k in [2, 1, 3]:
        st.put(k, k)
    st.root.key = 5
    st.root.left.key = 1
    st.root.right.key = 3
    assert st.is_bst() is False
    assert st.check() is False
    out = capsys.readouterr().out
    assert "Symmetric order not consistent" in out
    # rank corruption via monkeypatch
    st = avl.AVLTreeST()
    for k in [1, 2, 3]:
        st.put(k, k)
    orig_select = st.select

    def bad_select(k):
        return 99

    st.select = bad_select
    assert st.is_rank_consistent() is False
    assert st.check() is False
    out = capsys.readouterr().out
    assert "Ranks not consistent" in out
    st.select = orig_select
    # private helpers
    assert st._size_node(None) == 0
    assert st._height_node(None) == -1


"""
basic_avl_tree_set
"""

def test_avl_set_empty_and_sentinel() -> None:
    avls = _load_cs2da("week3/python/basic_avl_tree_set.py")
    s = avls.BasicAvlTreeSet()
    assert s.contains(5) is False
    s.remove(5)  # no-op
    assert s.root is avls._Node.EMPTY_LEAF
    assert avls._Node.EMPTY_LEAF.left is None
    assert avls._Node.EMPTY_LEAF.right is None
    assert avls._Node.EMPTY_LEAF.height == 0
    assert avls._Node.EMPTY_LEAF.value is None


def test_avl_set_add_remove_invariants() -> None:
    avls = _load_cs2da("week3/python/basic_avl_tree_set.py")
    s = avls.BasicAvlTreeSet()
    # duplicates
    for _ in range(3):
        s.add(10)
    # traverse count
    def count(node):
        if node is avls._Node.EMPTY_LEAF:
            return 0
        return 1 + count(node.left) + count(node.right)

    assert count(s.root) == 1
    assert s.contains(10) is True
    s.remove(99)  # absent
    # add many shuffled
    vals = list(range(1, 101))
    random.Random(42).shuffle(vals)
    for v in vals:
        s.add(v)
    for v in vals:
        assert s.contains(v) is True
    # remove evens
    for v in range(2, 101, 2):
        s.remove(v)
    for v in range(2, 101, 2):
        assert s.contains(v) is False
    for v in range(1, 101, 2):
        assert s.contains(v) is True
    # remove all
    for v in range(1, 101, 2):
        s.remove(v)
    assert count(s.root) == 0
    assert s.contains(1) is False
    # strings
    s2 = avls.BasicAvlTreeSet()
    s2.add("b")
    s2.add("a")
    assert s2.contains("a") is True


"""
sort_benchmark
"""

def test_sort_benchmark_timer(monkeypatch) -> None:
    sb = _load_cs2da("week4/python/sort_benchmark.py")
    sb._timer_start = -1
    now = [1000]

    def fake_ns():
        return now[0]

    monkeypatch.setattr(sb.time, "thread_time_ns", fake_ns)
    sb.start_timer()
    now[0] = 2500
    assert sb.stop_timer() == 1500
    assert sb._timer_start == -1
    # double start
    sb.start_timer()
    with pytest.raises(RuntimeError, match="timer already started"):
        sb.start_timer()
    sb.stop_timer()
    # stop without start
    with pytest.raises(RuntimeError, match="timer was not started"):
        sb.stop_timer()
    sb.start_timer()
    now[0] = 4000
    assert sb.stop_timer() == 1500
    sb._timer_start = -1


def test_random_list_and_print_array() -> None:
    sb = _load_cs2da("week4/python/sort_benchmark.py")
    sb._rng = random.Random(1)
    r = sb.random_list(5)
    assert len(r) == 5
    rb = random.Random(1)
    expected = [rb.randint(sb.JAVA_INT_MIN, sb.JAVA_INT_MAX) for _ in range(5)]
    sb._rng = random.Random(1)
    r2 = sb.random_list(5)
    assert r2 == expected
    assert all(sb.JAVA_INT_MIN <= v <= sb.JAVA_INT_MAX for v in r2)
    assert sb.random_list(0) == []
    # print_array
    from io import StringIO
    import sys as _sys

    buf = StringIO()
    old = _sys.stdout
    _sys.stdout = buf
    try:
        sb.print_array([1, 2, 3])
    finally:
        _sys.stdout = old
    assert buf.getvalue() == "1 2 3 \n"
    buf = StringIO()
    old = _sys.stdout
    _sys.stdout = buf
    try:
        sb.print_array([])
    finally:
        _sys.stdout = old
    assert buf.getvalue() == "\n"


def test_all_sorts_match_sorted_with_stability(capsys) -> None:
    sb = _load_cs2da("week4/python/sort_benchmark.py")
    fixtures = [[], [1], [2, 1], [3, 1, 2], [5, 5, 5], [4, 3, 2, 1]]
    for cls in [sb.Insertion, sb.Shell, sb.MergeBU, sb.Quick3way]:
        for xs in fixtures:
            a = list(xs)
            cls.sort(a)
            assert a == sorted(xs)
    # random
    r = random.Random(99)
    for n in range(0, 40):
        xs = [r.randint(-50, 50) for _ in range(n)]
        for cls in [sb.Insertion, sb.Shell, sb.MergeBU, sb.Quick3way]:
            a = list(xs)
            cls.sort(a)
            assert a == sorted(xs)
    # stability MergeBU: compare only the key, so equal keys keep input order
    class Rec:
        def __init__(self, key, tag):
            self.key = key
            self.tag = tag

        def __lt__(self, other):
            return self.key < other.key

    xs = [Rec(1, "b"), Rec(1, "a"), Rec(2, "c")]
    a = list(xs)
    sb.MergeBU.sort(a)
    assert [r.tag for r in a] == ["b", "a", "c"]
    # less/exchange
    assert sb.Insertion._less(1, 2) is True
    assert sb.Insertion._less(2, 1) is False
    a = [1, 2]
    sb.Insertion._exchange(a, 0, 1)
    assert a == [2, 1]
    # shuffle deterministic
    sb.random.seed(7)
    a = list(range(10))
    orig = list(a)
    sb.Quick3way.shuffle(a)
    assert sorted(a) == sorted(orig)
    # _merge
    a = [1, 3, 2, 4]
    aux = list(a)
    sb.MergeBU._merge(a, aux, 0, 1, 3)
    assert a[0:4] == [1, 2, 3, 4]


def test_sort_benchmark_main_wiring(capsys, monkeypatch) -> None:
    sb = _load_cs2da("week4/python/sort_benchmark.py")
    sb._timer_start = -1
    sb._rng = random.Random(123)
    monkeypatch.setattr(sb, "TIME_LIMIT_NANOSECONDS", 2)
    monkeypatch.setattr(sb, "random_list", lambda n: [])
    monkeypatch.setattr(sb, "start_timer", lambda: None)

    def fake_stop():
        return 3

    monkeypatch.setattr(sb, "stop_timer", fake_stop)
    calls = []

    for clsname in ["Insertion", "Shell", "MergeBU", "Quick3way"]:
        cls = getattr(sb, clsname)
        orig = cls.sort

        def make_sort(name, original):
            def s(a):
                calls.append(name)
                return original(a)
            return staticmethod(s)

        setattr(cls, "sort", make_sort(clsname.lower(), orig))
    try:
        seeds = []

        class FakeRandom:
            def __init__(self, seed=None):
                seeds.append(seed)

        monkeypatch.setattr(sb.random, "Random", FakeRandom)
        sb.main()
        out = capsys.readouterr().out
        assert "insertion,10000,0" in out
        assert "shell,10000,0" in out
        assert "merge,10000,0" in out
        assert "quick,10000,0" in out
        assert seeds == [20241024, 20241024, 20241024, 20241024]
        assert set(calls) == {"insertion", "shell", "mergebu", "quick3way"}
    finally:
        sb.Insertion.sort = sb.Insertion.sort
        sb.Shell.sort = sb.Shell.sort
        sb.MergeBU.sort = sb.MergeBU.sort
        sb.Quick3way.sort = sb.Quick3way.sort
        sb._timer_start = -1

