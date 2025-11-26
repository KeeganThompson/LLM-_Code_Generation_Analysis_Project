class SplayTree:
    """
    Implements a dictionary-like set for integers using a splay tree.

    A splay tree is a self-adjusting binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up and removal
    in O(log n) amortized time. This implementation stores unique integer keys.
    """

    class _Node:
        """A node in the splay tree."""
        __slots__ = 'key', 'parent', 'left', 'right'

        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty SplayTree."""
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
        """
        if not x:
            return
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
            elif x == parent.right and parent == grandparent.left:  # Zig-Zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (x is left child of right child)
                self._right_rotate(parent)
                self._left_rotate(grandparent)
        self.root = x

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        Performs the splaying operation on the accessed node (if the key is
        found) or its parent (if the key is not found) to move it to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
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

        # Key not found, splay the last visited node (parent of the null leaf).
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

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
                # Key already exists, splay it to the root and we're done.
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Insert new node as in a standard BST
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

        The tree is restructured after the deletion by splaying. If the key
        is not found, the last accessed node during the search is splayed.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node with the key (or its parent) to the root.
        self.search(key)

        # If the key is not at the root after splaying, it wasn't in the tree.
        if self.root.key != key:
            return

        # Now, the node to delete is at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        elif not right_subtree:
            # No right child, so the left subtree becomes the new tree.
            self.root = left_subtree
            if left_subtree:
                left_subtree.parent = None
        else:
            # Both children exist.
            # 1. Find the maximum node in the left subtree.
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right

            # 2. Splay this max node to the top of the left subtree.
            #    To do this, we temporarily set self.root to the left subtree's root.
            left_subtree.parent = None  # Detach left subtree

            self.root = left_subtree
            self._splay(max_in_left)

            # 3. self.root is now max_in_left. This is our new tree root.
            #    Attach the original right subtree to it.
            self.root.right = right_subtree
            right_subtree.parent = self.root