class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class provides a dictionary-like set for integers with `insert`, `delete`,
    and `search` methods. The key feature is the splaying operation, which moves
    an accessed node to the root of the tree, providing amortized logarithmic
    time complexity and optimizing for frequent access to the same elements.
    """

    class _Node:
        """A private inner class representing a node in the Splay Tree."""
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

    def _splay(self, node):
        """
        Performs the splay operation on a node, moving it to the root.
        This operation consists of a sequence of rotations (Zig, Zig-Zig, Zig-Zag)
        until the node becomes the root.
        """
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
            elif node == parent.right and parent == grandparent.right: # Zig-Zig case
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
        Searches for a key in the tree.

        This method performs the splaying operation on the accessed node (if found)
        or its would-be parent (if not found), moving it to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_accessed = None
        while current:
            last_accessed = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # If key is not found, splay the last accessed node (the parent).
        if last_accessed:
            self._splay(last_accessed)

        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key does not exist, a new node is created, inserted, and then
        splayed to the root.

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
                # Key already exists, splay it to the root and return.
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Key not found, insert new node.
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root.
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The tree is first searched for the key, which brings the node (or its
        potential parent) to the root. If the key is present at the root,
        it is removed and the two resulting subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        # Splay the node to be deleted (or its parent) to the root.
        if not self.search(key):
            # Key was not in the tree. search() already splayed the last
            # accessed node, so the tree is already rebalanced.
            return

        # At this point, the node to delete is the root, because search(key)
        # returned True, which means it found the key and splayed it.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Case 1: No left child. The right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Case 2: There is a left child.
            # Find the maximum element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum element to the root of the left subtree.
            # We temporarily set self.root to perform the splay within that subtree.
            left_subtree.parent = None
            self.root = left_subtree
            self._splay(max_node)

            # The new root (max_node) now has no right child.
            # Attach the original right subtree to it.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root