import sys

# Set a higher recursion limit for deep trees, although splaying keeps the tree balanced.
sys.setrecursionlimit(2000)

class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.

    Splay trees are self-balancing binary search trees with the additional property
    that recently accessed elements are quick to access again. They achieve this by
    moving any accessed node to the root of the tree through a series of rotations.

    This implementation includes the following methods:
    - insert(key): Adds a key to the tree.
    - delete(key): Removes a key from the tree.
    - search(key): Checks for the existence of a key.

    All three operations perform the splaying action as required.
    """

    class _Node:
        """A private helper class for the nodes of the Splay Tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on the given node x."""
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
        """Performs a right rotation on the given node x."""
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
        Performs the splaying operation on node x, moving it to the root.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:  # Zig-Zig case
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:  # Zig-Zig case
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            else:  # Zig-Zag case
                if x == parent.right and parent == grandparent.left:
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)
                else: # x == parent.left and parent == grandparent.right
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        Splays the found node to the root. If the key is not found,
        the last-accessed node (the would-be parent) is splayed to the root.
        Returns True if the key is found, False otherwise.
        """
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

        # Key not found, splay the last visited node if the tree is not empty.
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        If the key already exists, it is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and we are done.
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Insert the new node as a leaf.
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node to the root.
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        First, the key is searched, which brings the node (or its would-be parent)
        to the root. If the key is present, it is removed, and its inorder
        predecessor is splayed to become the new root.
        """
        # Search for the key. This will splay the node (or its parent) to the root.
        if not self.search(key):
            # Key not found. The would-be parent is already splayed.
            return

        # At this point, the node to delete is the root.
        node_to_delete = self.root

        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if not left_subtree:
            # If there's no left child, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree from the old root.
            left_subtree.parent = None

            # Find the maximum element in the left subtree (the inorder predecessor).
            new_root = left_subtree
            while new_root.right:
                new_root = new_root.right

            # Splay this maximum element to the root of the left subtree.
            # We can do this by temporarily setting the tree's root to the left subtree.
            self.root = left_subtree
            self._splay(new_root)
            # After splaying, self.root is new_root.

            # Attach the original right subtree to the new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root