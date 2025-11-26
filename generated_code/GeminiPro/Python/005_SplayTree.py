import sys

class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class implements a dictionary-like set for storing unique integer keys.
    It supports insert, delete, and search operations. The key feature of a
    splay tree is that any accessed node (or its parent if the node is not found)
    is moved to the root of thetree through a series of rotations, a process
    called "splaying". This ensures that frequently accessed elements are
    kept near the top of the tree, providing good amortized performance.

    The main methods are:
    - insert(key): Adds a key to the tree.
    - delete(key): Removes a key from the tree.
    - search(key): Checks for a key's existence and splays the accessed node.
    """

    class _Node:
        """A private helper class representing a node in the Splay Tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation around node x."""
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
            y.left = x
            x.parent = y

    def _right_rotate(self, x):
        """Performs a right rotation around node x."""
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
            y.right = x
            x.parent = y

    def _splay(self, node):
        """
        Performs the splaying operation on a node, moving it to the root.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig step
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zag-Zag
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zag-Zig
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def insert(self, key):
        """
        Inserts a key into the Splay Tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key does not exist, it is inserted and the new node becomes the root.

        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the closest node to the key's insertion point
        self.search(key)

        # After splaying, the root is the closest node.
        # If the key is already present, we're done.
        if self.root.key == key:
            return

        # Otherwise, insert the new key and make it the new root
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None

        self.root.parent = new_node
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the Splay Tree.

        If the key is found, its node is removed, and its parent is splayed
        to the root. If the key is not found, the last accessed node during
        the search is splayed.

        Args:
            key (int): The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node with the given key (or its would-be parent) to the root
        self.search(key)

        # If key is not in the tree, self.root.key will not match
        if self.root.key != key:
            return

        # Now, the node to be deleted is the root.
        # We need to join its left and right subtrees.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree to be the new root
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Find the maximum element in the left subtree
            left_subtree.parent = None
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this max element to the top of the left subtree
            # This makes it the new root of the merged tree
            self.root = left_subtree # Temporarily set root for splay
            self._splay(max_node)

            # Join the original right subtree
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root

    def search(self, key):
        """
        Searches for a key in the Splay Tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last node visited before reaching a NULL
        pointer is splayed to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = None
        while current:
            last_visited = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Key not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
        return False