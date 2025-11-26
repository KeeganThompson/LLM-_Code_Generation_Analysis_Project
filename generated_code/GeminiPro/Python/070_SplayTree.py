class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class implements a dictionary-like set for storing unique integer keys.
    It supports insert, delete, and search operations. The key feature is the
    splaying operation, which moves an accessed node to the root of the tree,
    optimizing for future accesses to the same node.
    """

    class Node:
        """A node in the splay tree."""
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
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:  # Zig-Zig (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:  # Zig-Zig (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:  # Zig-Zag (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag (right-left)
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
            bool: True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # If key is not found, splay the last visited node (if any)
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then the new node is splayed
        to the root.

        Args:
            key: The integer key to insert.
        """
        # Find position for new node, and check for duplicates
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay this node and return
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Insert the new node
        new_node = self.Node(key)
        new_node.parent = parent
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        First, the node with the given key is splayed to the root. If it
        doesn't exist, the nearest node is splayed and the function returns.
        If it exists, it is removed, and its two subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        # search() will splay the node (or its parent) to the root
        if not self.search(key):
            # Key was not in the tree, search already splayed the closest node
            return

        # At this point, the node to delete is the root because search(key) was True
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If no left child, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect left subtree to work on it
            left_subtree.parent = None

            # Find the maximum element in the left subtree
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right

            # Splay this maximum element to the root of the left subtree.
            # After this, the new root of the left subtree (max_in_left)
            # will have no right child. We achieve this by temporarily
            # setting the left subtree as the main tree to reuse _splay.
            self.root = left_subtree
            self._splay(max_in_left)

            # self.root is now the root of the modified left subtree.
            # We can now attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root