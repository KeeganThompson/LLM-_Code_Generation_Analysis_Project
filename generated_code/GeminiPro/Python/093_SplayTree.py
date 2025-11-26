class SplayTree:
    """
    A self-contained Splay Tree implementation for a set of integers.

    This class provides a dictionary-like set for integers with amortized
    O(log n) time complexity for insert, delete, and search operations.
    The key feature is the splaying operation, which moves frequently
    accessed elements closer to the root of the tree to optimize
    future accesses.

    Methods:
    - insert(key): Inserts an integer key into the set.
    - delete(key): Removes an integer key from the set.
    - search(key): Searches for a key and splays the accessed node (or its
                   parent if not found) to the root. Returns True if found,
                   False otherwise.
    """

    class _Node:
        """A private inner class for the nodes of the Splay Tree."""
        def __init__(self, key, parent=None, left=None, right=None):
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
        Performs the splaying operation on a node, moving it to the root.
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
            else:  # Zig-Zag case
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def insert(self, key):
        """
        Inserts a key into the splay tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.
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
                # Key already exists, splay it and return.
                self._splay(node)
                return

        # Insert the new node as a leaf
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node to the root
        self._splay(new_node)

    def search(self, key):
        """
        Searches for a key in the splay tree.

        Performs the splaying operation on the accessed node (if found)
        or its parent (if not found).

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        node = self.root
        last_node = None
        while node:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key found, splay the node
                self._splay(node)
                return True

        # Key not found, splay the last visited node (the parent)
        if last_node:
            self._splay(last_node)
        return False

    def delete(self, key):
        """
        Deletes a key from the splay tree.
        If the key is not found, the tree is splayed based on the last
        accessed node during the search, and no deletion occurs.
        """
        # Search for the key. This will splay the node (or its parent) to the root.
        if not self.search(key):
            # Key is not in the tree. search() has already splayed the closest node.
            return

        # After search(key), if the key was found, it is now at the root.
        # This check is implicitly true because search() returned True.
        # assert self.root.key == key

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # No right child, so the left subtree becomes the new tree
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both children exist. We will merge the two subtrees.
            # 1. Detach the left subtree from the old root.
            left_subtree.parent = None

            # 2. Find the maximum node in the left subtree.
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right

            # 3. Splay this maximum node to the top of the left subtree.
            #    To do this, we temporarily treat the left subtree as the main tree.
            self.root = left_subtree
            self._splay(max_in_left)

            # 4. The new root (max_in_left) now has no right child.
            #    Attach the original right subtree as its right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root