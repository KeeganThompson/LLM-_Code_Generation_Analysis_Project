class SplayTree:
    """
    A complete, self-contained Splay Tree class that implements a
    dictionary-like set for integers.

    The tree automatically rebalances itself by moving frequently accessed
    elements closer to the root through a process called "splaying".

    Methods:
    - insert(key): Adds an integer to the set.
    - delete(key): Removes an integer from the set.
    - search(key): Checks for an integer's presence and splays the accessed node.
    """

    class _Node:
        """A private inner class representing a node in the splay tree."""
        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _rotate_right(self, x: _Node):
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

    def _rotate_left(self, x: _Node):
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

    def _splay(self, node: _Node):
        """
        Splays the given node to the root of the tree through a series of
        rotations.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent

            if not grandparent:
                # Zig case: Parent is the root.
                if node == parent.left:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
            elif node == parent.left:
                if parent == grandparent.left:
                    # Zig-Zig case (left-left)
                    self._rotate_right(grandparent)
                    self._rotate_right(parent)
                else:
                    # Zig-Zag case (right-left)
                    self._rotate_right(parent)
                    self._rotate_left(grandparent)
            else:  # node is the right child
                if parent == grandparent.right:
                    # Zig-Zig case (right-right)
                    self._rotate_left(grandparent)
                    self._rotate_left(parent)
                else:
                    # Zig-Zag case (left-right)
                    self._rotate_left(parent)
                    self._rotate_right(grandparent)

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree.

        This method performs the splaying operation. If the key is found, the
        corresponding node is splayed to the root. If the key is not found,
        the last accessed node (the would-be parent) is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        current = self.root
        last_visited = None
        while current:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found, splay the node and return True
                self._splay(current)
                return True

        # Key not found, splay the last visited node (if any)
        if last_visited:
            self._splay(last_visited)

        return False

    def insert(self, key: int):
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
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and we're done
                self._splay(current)
                return

        # Insert new node
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key: int):
        """
        Deletes a key from the tree.

        The node containing the key (or its would-be parent) is first splayed
        to the root, and then the deletion is performed.

        Args:
            key: The integer key to delete.
        """
        # First, search for the key. This will splay the node to the root if it
        # exists, or its parent if it does not.
        self.search(key)

        # If the root does not hold the key, the key was not in the tree.
        if not self.root or self.root.key != key:
            return

        # At this point, the node to delete is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # The left subtree exists. We will make its largest element the new root.
            # 1. Disconnect the left subtree to work on it.
            left_subtree.parent = None

            # 2. Find the maximum node in the left subtree.
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right

            # 3. Splay this maximum node to the top of the left subtree.
            # To do this, we temporarily treat the left subtree as the main tree
            # so we can reuse the _splay method.
            self.root = left_subtree
            self._splay(max_in_left)

            # 4. After splaying, `self.root` is the new root of the combined tree.
            # This new root has no right child. We attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root