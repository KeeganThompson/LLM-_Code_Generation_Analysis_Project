class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class acts as a dictionary-like set for storing unique integer keys.
    Splay trees are self-balancing binary search trees with the property that
    recently accessed elements are quick to access again. This is achieved by
    moving any accessed, inserted, or deleted node to the root of the tree
    through a series of rotations, an operation called "splaying".
    """

    class _Node:
        """A private inner class representing a node in the Splay Tree."""
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

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.
        This operation consists of a series of rotations (Zig, Zig-Zig, Zig-Zag)
        until the node x is the root of the tree.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:
                # Zig-Zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:
                # Zig-Zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last non-null node visited during the
        search (the would-be parent) is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
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

        # Key not found, splay the last visited node if the tree was not empty
        if last_node:
            self._splay(last_node)

        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted as a new node and then that new node
        is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        # Case 1: Tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the closest node to the key's insertion point
        self.search(key)

        # Case 2: Key already exists, search has splayed it.
        if self.root.key == key:
            return

        # Case 3: Key does not exist, insert it and make it the new root.
        # The old root becomes a child of the new node.
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
        Deletes a key from the tree.

        The node with the given key (or its would-be parent) is first splayed
        to the root. If the key is present, the node is removed, and the
        remaining subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node to be deleted (or its parent) to the root
        self.search(key)

        # If the key is not in the tree, the root after splaying will not have the key
        if self.root.key != key:
            return

        # The node to be deleted is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree to be the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree from the old root
            left_subtree.parent = None

            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum node to the root of the left subtree.
            # We temporarily set self.root to the left subtree's root to reuse _splay.
            self.root = left_subtree
            self._splay(max_node)

            # After splaying, max_node is the new root. Its right child is None.
            # We attach the original right subtree to it.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root