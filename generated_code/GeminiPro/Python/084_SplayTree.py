import sys

class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree that functions
    as a dictionary-like set for integers.

    Splay trees are self-balancing binary search trees with the additional
    property that recently accessed elements are moved to the root of the tree,
    making subsequent accesses to them faster.
    """

    class _Node:
        """A private inner class representing a node in the splay tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
        y = x.right
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
        """Performs a right rotation on node x."""
        y = x.left
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
        Performs the splay operation on a node, moving it to the root.
        This operation consists of a series of rotations (Zig, Zig-Zig, Zig-Zag).
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-zig case
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-zig case
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-zag case (node is left, parent is right)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        This method performs the splaying operation on the accessed node if the key
        is found, or on its would-be parent if the key is not found.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise. After the call, the accessed
            node or its parent will be the new root of the tree.
        """
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

        # Key not found, splay the last visited node (the parent) if it exists.
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted as in a standard BST, and then the
        new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and we're done
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Insert the new node
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The deletion process involves splaying the node to the root, removing it,
        and then joining the two resulting subtrees.

        Args:
            key: The integer key to delete.
        """
        # First, search for the key. This will splay the node (if found) or
        # its parent (if not found) to the root.
        if not self.search(key):
            # Key was not in the tree. search() already splayed the would-be parent.
            return

        # At this point, the node to delete is guaranteed to be the root because
        # search(key) returned True.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree from the old root.
            left_subtree.parent = None

            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this max_node to the root of the (now isolated) left subtree.
            # We temporarily set the tree's root to the left subtree's root to
            # perform this splay operation correctly within that subtree.
            self.root = left_subtree
            self._splay(max_node)

            # After splaying, self.root is max_node. Now, attach the original
            # right subtree as the right child of this new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root