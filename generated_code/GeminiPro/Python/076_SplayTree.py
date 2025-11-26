class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class provides a dictionary-like set for storing unique integer keys.
    It supports insertion, deletion, and search operations. The key feature
    of a splay tree is that recently accessed elements are moved to the root
    of the tree, which can improve performance for certain access patterns.

    Methods:
        insert(key): Inserts a key into the tree.
        delete(key): Deletes a key from the tree.
        search(key): Searches for a key and splays the accessed node.
    """

    class Node:
        """A node in the splay tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    # --- Private Helper Methods for Tree Rotations and Splaying ---

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
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
        if y.right is not None:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
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
        """
        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent
            if grandparent is None:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    # --- Public API Methods ---

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the parent of the
        would-be key) is splayed to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        node = self.root
        last_visited = None
        while node is not None:
            last_visited = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Key not found, splay the last visited node if tree is not empty
        if last_visited is not None:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the splay tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        # Find position for new node (standard BST insert)
        parent = None
        current = self.root
        while current is not None:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and return
                self._splay(current)
                return

        # Insert the new node
        new_node = self.Node(key, parent)
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the splay tree.

        The node with the key (or its parent if not found) is first splayed
        to the root. If the key is found at the root, it is removed, and the
        remaining subtrees are joined.

        Args:
            key (int): The integer key to delete.
        """
        # search() will splay the node or its parent to the root
        if not self.search(key):
            # Key was not in the tree. search() splayed the closest node, so we're done.
            return

        # If search returned True, the node to delete is now the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if left_subtree is None:
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif right_subtree is None:
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. Join them.
            # Detach the left subtree to operate on it.
            left_subtree.parent = None

            # Find the maximum node in the left subtree.
            max_in_left = left_subtree
            while max_in_left.right is not None:
                max_in_left = max_in_left.right
            
            # Splay this max node to the root of its subtree.
            # We temporarily set self.root to the left subtree's root to
            # perform the splay operation within that subtree.
            self.root = left_subtree
            self._splay(max_in_left)
            # After splaying, self.root is max_in_left, which becomes the new
            # root of the combined tree.
            
            # Attach the original right subtree to the new root.
            self.root.right = right_subtree
            right_subtree.parent = self.root