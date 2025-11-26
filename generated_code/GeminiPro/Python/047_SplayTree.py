import sys

class SplayTree:
    """
    A self-contained Python class that implements a dictionary-like set for integers
    using a Splay Tree data structure.

    The tree automatically rebalances itself by moving frequently accessed elements
    closer to the root through a process called "splaying".

    Methods:
    - insert(key): Adds an integer key to the set.
    - delete(key): Removes an integer key from the set.
    - search(key): Checks for the existence of a key and splays the accessed node.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """Performs a right rotation on node x."""
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.
        """
        while x.parent is not None:
            p = x.parent
            g = p.parent
            if g is None:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-zig case (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-zig case (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-zag case (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-zag case (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def _maximum(self, node):
        """Finds the node with the maximum key in a subtree."""
        while node.right is not None:
            node = node.right
        return node

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the would-be parent)
        is splayed to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        last_node = None
        current = self.root
        while current is not None:
            last_node = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                self._splay(current)
                return True

        if last_node is not None:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        p = None
        current = self.root
        while current is not None:
            p = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and we are done.
                self._splay(current)
                return

        # Key is not in the tree, insert a new node
        new_node = self._Node(key)
        new_node.parent = p

        if p is None:  # The tree was empty
            self.root = new_node
        elif key < p.key:
            p.left = new_node
        else:
            p.right = new_node

        # Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The standard splay tree deletion algorithm is used:
        1. The node to be deleted is splayed to the root.
        2. The root is removed, splitting the tree into two subtrees.
        3. The maximum element of the left subtree is splayed to its root.
        4. The right subtree is attached as the right child of the new root.

        If the key is not found, the would-be parent is splayed as a side effect
        of the initial search.

        Args:
            key (int): The integer key to delete.
        """
        # Search for the key. This splays the node (or its parent) to the root.
        if not self.search(key):
            # Key was not in the tree. search() already splayed the parent.
            return

        # At this point, the node to delete is at the root because search(key)
        # returned True and splayed it.
        z = self.root
        left_subtree = z.left
        right_subtree = z.right

        if left_subtree is None and right_subtree is None:
            self.root = None
        elif left_subtree is None:
            self.root = right_subtree
            self.root.parent = None
        elif right_subtree is None:
            self.root = left_subtree
            self.root.parent = None
        else:
            # Both subtrees exist.
            # Detach the left subtree from the old root.
            left_subtree.parent = None

            # Find the maximum node in the left subtree.
            max_in_left = self._maximum(left_subtree)

            # Splay this max node to the root of the (now separated) left subtree.
            # We can do this by temporarily setting the tree's root to the left
            # subtree's root and then using the existing search/splay logic.
            self.root = left_subtree
            self.search(max_in_left.key)  # This splays max_in_left

            # After the splay, self.root is max_in_left, which has no right child.
            # Attach the original right subtree.
            self.root.right = right_subtree
            right_subtree.parent = self.root