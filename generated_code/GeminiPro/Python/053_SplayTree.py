import sys

# It can be good practice to increase the recursion limit for tree-based
# data structures, although this iterative implementation of splaying
# avoids deep recursion.
# sys.setrecursionlimit(2000)

class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class acts as a dictionary-like set for storing unique integer keys.
    It supports insertion, deletion, and searching. The key feature of a
    splay tree is that any accessed node (during search, insert, or delete)
    is moved to the root of the tree through a series of rotations, a process
    called "splaying". This makes recently accessed items faster to retrieve.
    """

    class _Node:
        """A private inner class representing a node in the splay tree."""
        __slots__ = 'key', 'parent', 'left', 'right'

        def __init__(self, key, parent=None, left=None, right=None):
            """Initializes a Node."""
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on the subtree rooted at node x."""
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
        """Performs a right rotation on the subtree rooted at node x."""
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

    def _splay(self, node):
        """
        Brings the given node to the root of the tree using splay operations.
        """
        if not node:
            return

        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig case
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig case
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (node is left, parent is right)
                self._right_rotate(parent)
                self._left_rotate(grandparent)
        self.root = node

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the corresponding node is splayed to the root, and
        True is returned. If the key is not found, the last non-null node
        accessed during the search (the would-be parent) is splayed to the
        root, and False is returned.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_node = None
        while current:
            last_node = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # If key was not found, splay the last accessed node.
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted as in a standard BST, and the new
        node is then splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay the node and we are done.
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        First, the key is searched for, which brings the node (or a nearby one)
        to the root. If the key is found at the root, it is removed. The two
        resulting subtrees are then merged by finding the maximum element in the
        left subtree, splaying it to its root, and then attaching the right
        subtree as its right child.

        Args:
            key (int): The integer key to delete.
        """
        # Splay the node with the given key (or its would-be parent) to the root.
        if not self.search(key):
            # Key not found. search() already splayed the closest node.
            return

        # At this point, if the key was found, it is at the root.
        # The check self.root.key == key confirms this.
        if self.root.key != key:
            return # Should not happen if search returned True, but is a safeguard.

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # The left subtree exists.
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node to the root of the (now separated) left subtree.
            # We temporarily set self.root to perform the splay within the subtree.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, self.root is max_node. It has no right child.
            # We can now attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root