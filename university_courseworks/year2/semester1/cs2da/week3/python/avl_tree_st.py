"""
Line-by-line Python translation of ``week3/java/AVLTreeST.java``.

The Java class is Sedgewick and Wayne's ordered symbol table, backed by an
AVL tree. It stores key-value pairs, supports the usual map operations, and
adds order statistics: minimum, maximum, floor, ceiling, select and rank.

Java to Python mapping used here:

  ``class AVLTreeST<Key, Value>``      -> ``class AVLTreeST(Generic[K, V])``
  ``Comparable<Key>.compareTo``        -> the ``<``, ``>`` and ``==`` operators
  ``private Node`` inner class         -> a module-level ``_Node`` class
  ``Queue<Key>``                       -> ``collections.deque``
  ``queue.enqueue(x)``                 -> ``queue.append(x)``
  ``queue.dequeue()``                  -> ``queue.popleft()``
  ``NoSuchElementException``           -> ``IndexError``
  ``IllegalArgumentException``         -> ``ValueError``
  ``StdOut.println``                   -> ``print``
  ``StdIn.readString()``               -> tokens from ``sys.stdin``

Java allows two methods with the same name and different parameters. Python
does not, so each private overload gains a descriptive suffix: the public
``min()`` stays ``min``, while the recursive ``min(Node x)`` becomes
``_min_node``. The same pattern applies to ``get``, ``put``, ``delete``,
``size``, ``height``, ``rank``, ``select``, ``keys``, ``floor`` and
``ceiling``.

Java's ``assert check()`` only runs when assertions are enabled with ``-ea``;
Python's ``assert`` only runs when ``__debug__`` is true. Both are therefore
development checks, and the tree remains correct without them.
"""

import sys
from collections import deque
from typing import Generic, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _Node:
    """
    Mirror of the Java inner ``Node`` class.

    ``__slots__`` fixes the set of attributes, which is the closest Python
    equivalent of Java's fixed field layout and avoids a per-instance
    ``__dict__``. Java's inner class also holds a hidden reference to the
    enclosing ``AVLTreeST``; the code never uses it, so this class does not
    carry one.
    """

    __slots__ = ("key", "value", "height", "size", "left", "right")

    def __init__(self, key: K, value: V, height: int, size: int) -> None:
        """
        Mirror of ``Node(Key key, Value val, int height, int size)``.

        ``left`` and ``right`` start as ``None``, which is the Python
        equivalent of Java's default ``null`` for object fields.
        """
        self.key = key
        self.value = value
        self.height = height
        self.size = size
        self.left: Optional["_Node"] = None
        self.right: Optional["_Node"] = None


class AVLTreeST(Generic[K, V]):
    """
    Mirror of the Java ``AVLTreeST`` class.

    The tree is a binary search tree in which every node's two subtrees
    differ in height by at most one. Rotations restore that property after
    an insertion or deletion.
    """

    def __init__(self) -> None:
        """Mirror of ``AVLTreeST()``: start with an empty tree."""
        self.root: Optional[_Node] = None

    def is_empty(self) -> bool:
        """Mirror of ``isEmpty``: true when there is no root node."""
        return self.root is None

    def size(self) -> int:
        """Mirror of the public ``size()``, which delegates to the node form."""
        return self._size_node(self.root)

    def _size_node(self, x: Optional[_Node]) -> int:
        """Mirror of the private ``size(Node x)``: zero for a missing node."""
        if x is None:
            return 0
        return x.size

    def height(self) -> int:
        """Mirror of the public ``height()``."""
        return self._height_node(self.root)

    def _height_node(self, x: Optional[_Node]) -> int:
        """
        Mirror of the private ``height(Node x)``.

        An empty tree has height -1 and a single node has height 0, so a
        missing node returns -1 rather than 0.
        """
        if x is None:
            return -1
        return x.height

    def get(self, key: K) -> Optional[V]:
        """
        Mirror of the public ``get(Key key)``.

        Returns ``None`` when the key is absent. In this symbol table a
        ``None`` value cannot be stored: ``put`` treats it as a deletion, so
        the return value is unambiguous.
        """
        if key is None:
            raise ValueError("argument to get() is null")
        x = self._get_node(self.root, key)
        if x is None:
            return None
        return x.value

    def _get_node(self, x: Optional[_Node], key: K) -> Optional[_Node]:
        """
        Mirror of the private ``get(Node x, Key key)``.

        The comparison decides which way to descend. The recursive calls
        mirror the Java returns one for one.
        """
        if x is None:
            return None
        if key < x.key:
            return self._get_node(x.left, key)
        if key > x.key:
            return self._get_node(x.right, key)
        return x

    def contains(self, key: K) -> bool:
        """Mirror of ``contains``: a key is present when ``get`` finds a node."""
        return self.get(key) is not None

    def put(self, key: K, value: Optional[V]) -> None:
        """
        Mirror of ``put(Key key, Value val)``.

        A ``None`` value deletes the key, exactly as the Java documentation
        describes. The root is replaced by whatever the recursive insert
        returns, because a rotation can change which node is at the top.
        """
        if key is None:
            raise ValueError("first argument to put() is null")
        if value is None:
            self.delete(key)
            return
        self.root = self._put_node(self.root, key, value)
        assert self.check()

    def _put_node(self, x: Optional[_Node], key: K, value: V) -> _Node:
        """
        Mirror of the private ``put(Node x, Key key, Value val)``.

        A missing child becomes the new node. An existing key has its value
        replaced and is returned unchanged, without a size or height update.
        After a real insertion, the size and height are recomputed and the
        subtree is rebalanced.
        """
        if x is None:
            return _Node(key, value, 0, 1)

        if key < x.key:
            x.left = self._put_node(x.left, key, value)
        elif key > x.key:
            x.right = self._put_node(x.right, key, value)
        else:
            x.value = value
            return x

        x.size = 1 + self._size_node(x.left) + self._size_node(x.right)
        x.height = 1 + max(self._height_node(x.left),
                           self._height_node(x.right))
        return self._balance(x)

    def _balance(self, x: _Node) -> _Node:
        """
        Mirror of ``balance``: restore the AVL property after a change.

        A balance factor below -1 means the right side is too tall. If the
        right child leans left, a right rotation on it comes first; that is
        the double-rotation case. The mirror case handles a left-heavy node.
        """
        if self._balance_factor(x) < -1:
            if self._balance_factor(x.right) > 0:
                x.right = self._rotate_right(x.right)
            x = self._rotate_left(x)
        elif self._balance_factor(x) > 1:
            if self._balance_factor(x.left) < 0:
                x.left = self._rotate_left(x.left)
            x = self._rotate_right(x)
        return x

    def _balance_factor(self, x: _Node) -> int:
        """
        Mirror of ``balanceFactor``: left height minus right height.

        A value of -1, 0 or 1 satisfies the AVL property.
        """
        return self._height_node(x.left) - self._height_node(x.right)

    def _rotate_right(self, x: _Node) -> _Node:
        """
        Mirror of ``rotateRight``.

        ``y`` becomes the new subtree root, ``x`` becomes its right child,
        and ``y``'s old right child becomes ``x``'s left child. Sizes are
        updated before heights, because the height calculation reads sizes
        only indirectly through the children that have already been fixed.
        """
        y = x.left
        x.left = y.right
        y.right = x

        y.size = x.size
        x.size = 1 + self._size_node(x.left) + self._size_node(x.right)
        x.height = 1 + max(self._height_node(x.left),
                           self._height_node(x.right))
        y.height = 1 + max(self._height_node(y.left),
                           self._height_node(y.right))
        return y

    def _rotate_left(self, x: _Node) -> _Node:
        """Mirror of ``rotateLeft``, the mirror image of ``rotateRight``."""
        y = x.right
        x.right = y.left
        y.left = x

        y.size = x.size
        x.size = 1 + self._size_node(x.left) + self._size_node(x.right)
        x.height = 1 + max(self._height_node(x.left),
                           self._height_node(x.right))
        y.height = 1 + max(self._height_node(y.left),
                           self._height_node(y.right))
        return y

    def delete(self, key: K) -> None:
        """
        Mirror of ``delete(Key key)``.

        Deleting a key that is not present is a no-op. The ``contains`` check
        is what lets the recursive form assume it has found a node.
        """
        if key is None:
            raise ValueError("argument to delete() is null")
        if not self.contains(key):
            return
        self.root = self._delete_node(self.root, key)
        assert self.check()

    def _delete_node(self, x: _Node, key: K) -> Optional[_Node]:
        """
        Mirror of the private ``delete(Node x, Key key)``.

        A node with one child is replaced by that child. A node with two
        children is replaced by its successor, the minimum of its right
        subtree, and that successor is then removed from the right subtree.
        """
        if key < x.key:
            x.left = self._delete_node(x.left, key)
        elif key > x.key:
            x.right = self._delete_node(x.right, key)
        else:
            if x.left is None:
                return x.right
            if x.right is None:
                return x.left
            y = x
            x = self._min_node(y.right)
            x.right = self._delete_min_node(y.right)
            x.left = y.left

        x.size = 1 + self._size_node(x.left) + self._size_node(x.right)
        x.height = 1 + max(self._height_node(x.left),
                           self._height_node(x.right))
        return self._balance(x)

    def delete_min(self) -> None:
        """Mirror of ``deleteMin()``, raising ``IndexError`` when empty."""
        if self.is_empty():
            raise IndexError("called deleteMin() with empty symbol table")
        self.root = self._delete_min_node(self.root)
        assert self.check()

    def _delete_min_node(self, x: _Node) -> Optional[_Node]:
        """
        Mirror of the private ``deleteMin(Node x)``.

        The leftmost node is the minimum. Its right child takes its place,
        and the ancestors are rebalanced on the way back up.
        """
        if x.left is None:
            return x.right
        x.left = self._delete_min_node(x.left)
        x.size = 1 + self._size_node(x.left) + self._size_node(x.right)
        x.height = 1 + max(self._height_node(x.left),
                           self._height_node(x.right))
        return self._balance(x)

    def delete_max(self) -> None:
        """Mirror of ``deleteMax()``, raising ``IndexError`` when empty."""
        if self.is_empty():
            raise IndexError("called deleteMax() with empty symbol table")
        self.root = self._delete_max_node(self.root)
        assert self.check()

    def _delete_max_node(self, x: _Node) -> Optional[_Node]:
        """Mirror of the private ``deleteMax(Node x)``."""
        if x.right is None:
            return x.left
        x.right = self._delete_max_node(x.right)
        x.size = 1 + self._size_node(x.left) + self._size_node(x.right)
        x.height = 1 + max(self._height_node(x.left),
                           self._height_node(x.right))
        return self._balance(x)

    def min(self) -> K:
        """Mirror of the public ``min()``: the smallest key in the tree."""
        if self.is_empty():
            raise IndexError("called min() with empty symbol table")
        return self._min_node(self.root).key

    def _min_node(self, x: _Node) -> _Node:
        """Mirror of the private ``min(Node x)``: follow left children."""
        if x.left is None:
            return x
        return self._min_node(x.left)

    def max(self) -> K:
        """Mirror of the public ``max()``: the largest key in the tree."""
        if self.is_empty():
            raise IndexError("called max() with empty symbol table")
        return self._max_node(self.root).key

    def _max_node(self, x: _Node) -> _Node:
        """Mirror of the private ``max(Node x)``: follow right children."""
        if x.right is None:
            return x
        return self._max_node(x.right)

    def floor(self, key: K) -> Optional[K]:
        """
        Mirror of ``floor(Key key)``.

        Returns the largest stored key less than or equal to ``key``, or
        ``None`` when every key is larger.
        """
        if key is None:
            raise ValueError("argument to floor() is null")
        if self.is_empty():
            raise IndexError("called floor() with empty symbol table")
        x = self._floor_node(self.root, key)
        if x is None:
            return None
        return x.key

    def _floor_node(self, x: Optional[_Node], key: K) -> Optional[_Node]:
        """
        Mirror of the private ``floor(Node x, Key key)``.

        When the key is smaller than the current node, the answer can only be
        on the left. Otherwise the best candidate may be the current node, and
        a result from the right subtree takes precedence when one exists.
        """
        if x is None:
            return None
        if key == x.key:
            return x
        if key < x.key:
            return self._floor_node(x.left, key)
        y = self._floor_node(x.right, key)
        if y is not None:
            return y
        return x

    def ceiling(self, key: K) -> Optional[K]:
        """
        Mirror of ``ceiling(Key key)``.

        Returns the smallest stored key greater than or equal to ``key``, or
        ``None`` when every key is smaller.
        """
        if key is None:
            raise ValueError("argument to ceiling() is null")
        if self.is_empty():
            raise IndexError("called ceiling() with empty symbol table")
        x = self._ceiling_node(self.root, key)
        if x is None:
            return None
        return x.key

    def _ceiling_node(self, x: Optional[_Node], key: K) -> Optional[_Node]:
        """Mirror of the private ``ceiling(Node x, Key key)``."""
        if x is None:
            return None
        if key == x.key:
            return x
        if key > x.key:
            return self._ceiling_node(x.right, key)
        y = self._ceiling_node(x.left, key)
        if y is not None:
            return y
        return x

    def select(self, k: int) -> K:
        """
        Mirror of ``select(int k)``: the kth smallest key, counting from zero.

        The range check is what turns an out-of-range index into a clear
        error before the recursive form dereferences a missing node.
        """
        if k < 0 or k >= self.size():
            raise ValueError(f"k is not in range 0-{self.size() - 1}")
        x = self._select_node(self.root, k)
        return x.key

    def _select_node(self, x: Optional[_Node], k: int) -> Optional[_Node]:
        """
        Mirror of the private ``select(Node x, int k)``.

        ``t`` is the number of keys to the left. If ``t`` is smaller than
        ``k``, the target is in the right subtree at position ``k - t - 1``.
        """
        if x is None:
            return None
        t = self._size_node(x.left)
        if t > k:
            return self._select_node(x.left, k)
        if t < k:
            return self._select_node(x.right, k - t - 1)
        return x

    def rank(self, key: K) -> int:
        """
        Mirror of the public ``rank(Key key)``.

        Counts keys strictly smaller than ``key``. The public form takes the
        key only and passes a ``None`` node check down to the recursive form.
        """
        if key is None:
            raise ValueError("argument to rank() is null")
        return self._rank_node(key, self.root)

    def _rank_node(self, key: K, x: Optional[_Node]) -> int:
        """
        Mirror of the private ``rank(Key key, Node x)``.

        A match adds the size of the left subtree. A larger key adds one for
        the current node plus everything to its left.
        """
        if x is None:
            return 0
        if key < x.key:
            return self._rank_node(key, x.left)
        if key > x.key:
            return 1 + self._size_node(x.left) + self._rank_node(key, x.right)
        return self._size_node(x.left)

    def keys(self) -> list[K]:
        """Mirror of ``keys()``: all keys in ascending order."""
        return self.keys_in_order()

    def keys_in_order(self) -> list[K]:
        """
        Mirror of ``keysInOrder()``.

        Java returns a ``Queue<Key>`` that is iterated; a Python list is the
        natural equivalent and supports the same ``for`` loop.
        """
        queue: deque[K] = deque()
        self._keys_in_order_node(self.root, queue)
        return list(queue)

    def _keys_in_order_node(self, x: Optional[_Node], queue: deque[K]) -> None:
        """Mirror of the private ``keysInOrder``: left, node, right."""
        if x is None:
            return
        self._keys_in_order_node(x.left, queue)
        queue.append(x.key)
        self._keys_in_order_node(x.right, queue)

    def keys_level_order(self) -> list[K]:
        """
        Mirror of ``keysLevelOrder()``.

        Two queues are used: one holds nodes in breadth-first order and the
        other collects their keys. ``deque.popleft`` is Java's ``dequeue``.
        """
        queue: deque[K] = deque()
        if not self.is_empty():
            queue2: deque[_Node] = deque()
            queue2.append(self.root)
            while queue2:
                x = queue2.popleft()
                queue.append(x.key)
                if x.left is not None:
                    queue2.append(x.left)
                if x.right is not None:
                    queue2.append(x.right)
        return list(queue)

    def keys_range(self, lo: K, hi: K) -> list[K]:
        """
        Mirror of ``keys(Key lo, Key hi)``.

        The Java overload is renamed here because Python cannot have two
        methods called ``keys``. Keys are returned from ``lo`` inclusive to
        ``hi`` exclusive.
        """
        if lo is None:
            raise ValueError("first argument to keys() is null")
        if hi is None:
            raise ValueError("second argument to keys() is null")
        queue: deque[K] = deque()
        self._keys_range_node(self.root, queue, lo, hi)
        return list(queue)

    def _keys_range_node(self, x: Optional[_Node], queue: deque[K],
                         lo: K, hi: K) -> None:
        """
        Mirror of the private ``keys`` overload.

        The two comparisons decide whether the left subtree, the current node
        or the right subtree can contain keys in the range. Pruning the
        subtrees this way is what keeps the operation O(log n + k).
        """
        if x is None:
            return
        cmplo = lo < x.key
        cmphi = hi > x.key
        if cmplo:
            self._keys_range_node(x.left, queue, lo, hi)
        if not (lo > x.key) and not (hi < x.key):
            queue.append(x.key)
        if cmphi:
            self._keys_range_node(x.right, queue, lo, hi)

    def size_range(self, lo: K, hi: K) -> int:
        """
        Mirror of ``size(Key lo, Key hi)``.

        Renamed for the same reason as ``keys_range``. The upper bound is
        included when it is present and excluded when it is absent, matching
        the Java arithmetic.
        """
        if lo is None:
            raise ValueError("first argument to size() is null")
        if hi is None:
            raise ValueError("second argument to size() is null")
        if lo > hi:
            return 0
        if self.contains(hi):
            return self.rank(hi) - self.rank(lo) + 1
        return self.rank(hi) - self.rank(lo)

    def check(self) -> bool:
        """
        Mirror of ``check``.

        Each invariant is tested and reported separately, then all four are
        re-tested for the return value. The repeated calls are deliberate:
        the Java version prints before deciding, so a failure is visible even
        when the caller ignores the boolean.
        """
        if not self.is_bst():
            print("Symmetric order not consistent")
        if not self.is_avl():
            print("AVL property not consistent")
        if not self.is_size_consistent():
            print("Subtree counts not consistent")
        if not self.is_rank_consistent():
            print("Ranks not consistent")
        return (self.is_bst() and self.is_avl()
                and self.is_size_consistent() and self.is_rank_consistent())

    def is_avl(self) -> bool:
        """Mirror of the public ``isAVL()``."""
        return self._is_avl_node(self.root)

    def _is_avl_node(self, x: Optional[_Node]) -> bool:
        """Mirror of the private ``isAVL(Node x)``."""
        if x is None:
            return True
        bf = self._balance_factor(x)
        if bf > 1 or bf < -1:
            return False
        return self._is_avl_node(x.left) and self._is_avl_node(x.right)

    def is_bst(self) -> bool:
        """Mirror of the public ``isBST()``: start with no bounds."""
        return self._is_bst_node(self.root, None, None)

    def _is_bst_node(self, x: Optional[_Node], min_key: Optional[K],
                     max_key: Optional[K]) -> bool:
        """
        Mirror of the private ``isBST(Node x, Key min, Key max)``.

        A ``None`` bound means that side is unconstrained. The recursive
        calls tighten the bounds with the current key, so the whole tree is
        checked rather than only adjacent pairs.
        """
        if x is None:
            return True
        if min_key is not None and x.key <= min_key:
            return False
        if max_key is not None and x.key >= max_key:
            return False
        return (self._is_bst_node(x.left, min_key, x.key)
                and self._is_bst_node(x.right, x.key, max_key))

    def is_size_consistent(self) -> bool:
        """Mirror of the public ``isSizeConsistent()``."""
        return self._is_size_consistent_node(self.root)

    def _is_size_consistent_node(self, x: Optional[_Node]) -> bool:
        """Mirror of the private ``isSizeConsistent(Node x)``."""
        if x is None:
            return True
        if x.size != self._size_node(x.left) + self._size_node(x.right) + 1:
            return False
        return (self._is_size_consistent_node(x.left)
                and self._is_size_consistent_node(x.right))

    def is_rank_consistent(self) -> bool:
        """
        Mirror of ``isRankConsistent``.

        ``select(rank(k))`` must return ``k`` and ``rank(select(i))`` must
        return ``i``. Java compares keys with ``compareTo() != 0``; Python's
        ``!=`` is the equivalent for the ordered key types this table uses.
        """
        for i in range(self.size()):
            if i != self.rank(self.select(i)):
                return False
        for key in self.keys():
            if key != self.select(self.rank(key)):
                return False
        return True


def main() -> None:
    """
    Mirror of ``AVLTreeST.main``.

    Java reads one string at a time from ``StdIn`` until it is empty. Python
    reads the whole of standard input and splits it into tokens, which gives
    the same sequence for the sample file.
    """
    st: AVLTreeST[str, int] = AVLTreeST()
    for i, key in enumerate(sys.stdin.read().split()):
        st.put(key, i)
    for s in st.keys():
        print(f"{s} {st.get(s)}")
    print()


if __name__ == "__main__":
    main()

