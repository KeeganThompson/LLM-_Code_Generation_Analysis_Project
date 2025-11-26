import sys

class SplayTree:
    """
    A complete, self-contained Python class that implements a splay tree.
    This class functions as a dictionary-like set for storing unique integer keys.

    Splay trees are self-balancing binary search trees with the property that
    recently accessed elements are moved to the root of the tree, allowing for
    faster subsequent access.

    Attributes:
        root (Node): The root node of the splay tree.
    """

    class _Node:
        """A private inner class representing a node in the splay tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
            y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """Performs a right rotation on node x."""
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.
        This is the core operation that maintains the tree's balance and
        amortized efficiency.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig case (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig case (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag case (right-left)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag case (left-right)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last non-null node on the search path is
        splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise. After the call, the
            accessed node (or its parent) will be the new root.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # If key is not found, splay the last visited node.
        if last_node:
            self._splay(last_node)

        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted as a new node and then splayed to
        the root, becoming the new root of the tree.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key already exists, splay the found node and return
                self._splay(node)
                return

        # Key doesn't exist, so insert it
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The tree is first splayed on the key. If the key is found at the root,
        it is removed. The tree is then re-formed by joining the left and
        right subtrees. The largest element in the left subtree is splayed to
        its root and becomes the new root of the combined tree.

        Args:
            key: The integer key to delete.
        """
        # Splay the node to the root (or its parent if not found)
        if not self.search(key):
            # Key was not in the tree. search() already splayed the closest node.
            return

        # After search(key) returns True, the node with the key is at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree from the old root
            left_subtree.parent = None

            # Find the maximum node in the left subtree. This will be the new root.
            new_root = left_subtree
            while new_root.right:
                new_root = new_root.right

            # Splay this maximum node to the top of the left subtree.
            # To do this, we temporarily treat the left subtree as the whole tree.
            self.root = left_subtree
            self._splay(new_root)

            # After splaying, self.root is the new root of the (former) left subtree.
            # This new root is guaranteed to have no right child.
            # Attach the original right subtree as its right child.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root