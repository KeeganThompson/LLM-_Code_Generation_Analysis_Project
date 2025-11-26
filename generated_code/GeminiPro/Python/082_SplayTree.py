class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class implements a dictionary-like set for storing unique integers.
    The main operations (insert, delete, search) are amortized O(log n).

    The key feature of a splay tree is that recently accessed elements are
    quick to access again. This is achieved by the "splay" operation, which
    moves an accessed node to the root of the tree.
    """

    class _Node:
        """A node in the Splay Tree."""
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
        Splays the node x to the root of the tree.
        This operation moves the node x up the tree through a series of
        rotations until it becomes the new root.
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
                # Zig-zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:
                # Zig-zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:
                # Zig-zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:
                # Zig-zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the would-be parent)
        is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_visited = None
        while node:
            last_visited = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key found, splay the node and return True
                self._splay(node)
                return True

        # Key not found. Splay the last visited node if the tree is not empty.
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key does not exist, it is inserted and the new node is splayed
        to the root. If the key already exists, the existing node is splayed
        to the root.

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
                # Key already exists, splay it and return
                self._splay(node)
                return

        # Key does not exist, create a new node
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

        The standard splay tree deletion algorithm is used:
        1. Search for the key. This brings the node (or a neighbor) to the root.
        2. If the key is at the root, remove it.
        3. Join the two resulting subtrees (left and right). This is done by
           finding the maximum element in the left subtree, splaying it to the
           root of the left subtree, and then making the right subtree its
           right child.

        Args:
            key: The integer key to delete.
        """
        # First, search for the key. This will splay the node to the root if found,
        # or its would-be parent if not found.
        if not self.search(key):
            # Key was not in the tree. search() already splayed the last
            # accessed node, so we can just return.
            return

        # At this point, the node to delete is the root.
        assert self.root.key == key

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # No right child, the left subtree becomes the new tree
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both children exist. We need to join the two subtrees.
            # 1. Isolate the left subtree.
            self.root = left_subtree
            self.root.parent = None

            # 2. Find the maximum node in this new temporary tree (the old left subtree).
            max_node = self.root
            while max_node.right:
                max_node = max_node.right

            # 3. Splay this max node to the root of the temporary tree.
            self._splay(max_node)

            # 4. After splaying, self.root is the max_node, which has no right child.
            #    Attach the original right subtree as its right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root