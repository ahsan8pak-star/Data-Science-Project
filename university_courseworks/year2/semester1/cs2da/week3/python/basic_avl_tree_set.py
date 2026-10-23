"""
Line-by-line Python translation of ``week3/java/BasicAvlTreeSet.java``.

The Java class is Project Nayuki's minimal AVL tree set (MIT licence, as
stated in the original header). It stores unique comparable values, and each
node carries its own height so that rebalancing needs no separate metadata.

Java to Python mapping used here:

  ``BasicAvlTreeSet<E extends Comparable<? super E>>`` -> ``Generic[E]``
  ``private static final class Node<E>``               -> module-level ``_Node``
  ``Node.EMPTY_LEAF``                                  -> ``_Node.EMPTY_LEAF``
  ``this == EMPTY_LEAF``                               -> ``self is _Node.EMPTY_LEAF``
  ``@SuppressWarnings({"unchecked","rawtypes"})``     -> no equivalent needed
  ``Math.max(a, b)``                                   -> ``max(a, b)``

The sentinel deserves a note. Java creates one ``EMPTY_LEAF`` node and makes
every real node point its missing children at it, so the recursive methods
never have to check for ``null``. The sentinel's own ``left`` and ``right``
are ``null``, because the static field is still being initialised when its
constructor runs. Python reproduces that exactly: the class attribute is
``None`` until ``_Node.EMPTY_LEAF = _Node()`` runs, so the sentinel is built
with ``None`` children while every later node gets the sentinel. The methods
never read the sentinel's children, which is why the difference is harmless.

Every comparison against the sentinel is an identity test (``is``), never
value equality (``==``). Java's ``==`` on objects is identity, and a node
holds no value that could sensibly be compared anyway.
"""

from typing import Generic, Optional, TypeVar

E = TypeVar("E")


class _Node(Generic[E]):
    """
    Mirror of the Java ``Node`` inner class.

    ``__slots__`` fixes the four fields, matching Java's fixed layout. The
    class attribute ``EMPTY_LEAF`` is assigned after the class body, which is
    the same order Java uses for its static initialiser.
    """

    __slots__ = ("value", "height", "left", "right")

    # Filled in immediately after the class definition. It is None while the
    # sentinel itself is being constructed, exactly as in Java.
    EMPTY_LEAF: Optional["_Node"] = None

    def __init__(self) -> None:
        """
        Mirror of the implicit ``Node()`` constructor.

        Java's field initialisers are ``value = null``, ``height = 0`` and
        both children pointing at ``EMPTY_LEAF``. For the sentinel those
        children resolve to ``null``; for every other node they resolve to
        the sentinel.
        """
        self.value: Optional[E] = None
        self.height = 0
        self.left: Optional["_Node"] = _Node.EMPTY_LEAF
        self.right: Optional["_Node"] = _Node.EMPTY_LEAF

    def add(self, val: E) -> "_Node[E]":
        """
        Mirror of ``Node.add``.

        Adding to the sentinel creates a real leaf of height 1. Otherwise the
        value descends left or right, and an equal value is ignored, which is
        what makes this a set rather than a multiset.
        """
        if self is _Node.EMPTY_LEAF:
            result = _Node()
            result.value = val
            result.height = 1
            return result
        if val < self.value:
            self.left = self.left.add(val)
        elif val > self.value:
            self.right = self.right.add(val)
        # The recalculate-then-balance order is required: balance() reads the
        # children's heights, so this node's own height must be current first.
        return self._recalculate()._balance()

    def remove(self, val: E) -> "_Node[E]":
        """
        Mirror of ``Node.remove``.

        Removing from the sentinel returns the sentinel. A node with two
        children is overwritten with its successor, the leftmost value of its
        right subtree, and that successor is then removed from the right
        subtree. A node with at most one child is replaced by that child.
        """
        if self is _Node.EMPTY_LEAF:
            return self
        if val < self.value:
            self.left = self.left.remove(val)
        elif val > self.value:
            self.right = self.right.remove(val)
        elif (self.left is not _Node.EMPTY_LEAF
              and self.right is not _Node.EMPTY_LEAF):
            temp = self.right
            # Java's for loop has an empty body: walk to the leftmost node.
            while temp.left is not _Node.EMPTY_LEAF:
                temp = temp.left
            self.value = temp.value
            self.right = self.right.remove(self.value)
        else:
            # At most one child: splice it in. With two empty children the
            # right leaf is returned, which is the same as the left one.
            return (self.right if self.left is _Node.EMPTY_LEAF
                    else self.left)
        return self._recalculate()._balance()

    def _balance(self) -> "_Node[E]":
        """
        Mirror of ``balance``.

        A height difference of -2 means the right subtree is taller, so the
        node is rotated left. A difference of +1 in the left child means the
        left subtree leans right, so that child is rotated right first. The
        positive case is the mirror image.
        """
        result: "_Node[E]" = self
        if self.right.height - self.left.height == -2:
            if self.left.right.height - self.left.left.height == 1:
                self.left = self.left._rotate_left()
            result = self._rotate_right()
        elif self.right.height - self.left.height == 2:
            if self.right.right.height - self.right.left.height == -1:
                self.right = self.right._rotate_right()
            result = self._rotate_left()
        return result

    def _rotate_left(self) -> "_Node[E]":
        """
        Mirror of ``rotateLeft``.

        The right child becomes the new root. Its left subtree moves to the
        old root's right, and the old root becomes its left child. Both nodes
        are recalculated, because their subtree heights have changed.
        """
        root = self.right
        self.right = root.left
        root.left = self._recalculate()
        return root._recalculate()

    def _rotate_right(self) -> "_Node[E]":
        """Mirror of ``rotateRight``, the mirror image of ``rotateLeft``."""
        root = self.left
        self.left = root.right
        root.right = self._recalculate()
        return root._recalculate()

    def _recalculate(self) -> "_Node[E]":
        """
        Mirror of ``recalculate``: height one greater than the taller child.

        The sentinel keeps height 0, so a real leaf gets height 1 without a
        special case. Returning ``self`` lets callers chain ``balance``.
        """
        self.height = max(self.left.height, self.right.height) + 1
        return self


# Java: public static final Node EMPTY_LEAF = new Node();
# Assigned after the class so __init__ sees None while building the sentinel.
_Node.EMPTY_LEAF = _Node()


class BasicAvlTreeSet(Generic[E]):
    """
    Mirror of the Java ``BasicAvlTreeSet`` class.

    A set built on the AVL nodes above. Java marks the class ``final``; Python
    has no equivalent keyword, so the class is simply left unsubclassed.
    """

    def __init__(self) -> None:
        """Mirror of the field initialiser ``root = EMPTY_LEAF``."""
        self.root = _Node.EMPTY_LEAF

    def contains(self, val: E) -> bool:
        """
        Mirror of ``contains``.

        The loop descends until it finds the value or reaches the sentinel.
        Python's ``for`` cannot express "walk a linked structure" without a
        helper, so the Java ``for`` becomes a ``while`` with the same update.
        """
        node = self.root
        while node is not _Node.EMPTY_LEAF:
            if val < node.value:
                node = node.left
            elif val > node.value:
                node = node.right
            else:
                return True
        return False

    def add(self, val: E) -> None:
        """
        Mirror of ``add``.

        The root is replaced by whatever the recursive insert returns,
        because a rotation can put a different node at the top.
        """
        self.root = self.root.add(val)

    def remove(self, val: E) -> None:
        """Mirror of ``remove``: the same root replacement as ``add``."""
        self.root = self.root.remove(val)

