class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class implements a dictionary-like set for storing unique integer keys.
    It supports insert, delete, and search operations. The key feature of a
    splay tree is that recently accessed elements are moved to the root of the
    tree, which can improve performance for certain access patterns (locality
    of reference).
    """

    class _Node:
        """A private class representing a node in the Splay Tree."""
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _right_rotate(self, node):
        """Performs a right rotation on the given node."""
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        return new_root

    def _left_rotate(self, node):
        """Performs a left rotation on the given node."""
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        return new_root

    def _splay(self, key):
        """
        Splays the node with the given key to the root.

        If the key is not in the tree, the last accessed node on the search
        path is splayed to the root. This is a top-down splay implementation.
        """
        if not self.root or self.root.key == key:
            return

        # Use a dummy node to simplify linking of Left and Right subtrees
        dummy = self._Node(None)
        left_tree_max = dummy
        right_tree_min = dummy
        current = self.root

        while True:
            if key < current.key:
                if not current.left:
                    break
                # Zig-Zig case (left-left)
                if key < current.left.key:
                    current = self._right_rotate(current)
                    if not current.left:
                        break
                # Link current to the right tree (nodes larger than key)
                right_tree_min.left = current
                right_tree_min = current
                current = current.left
            elif key > current.key:
                if not current.right:
                    break
                # Zig-Zig case (right-right)
                if key > current.right.key:
                    current = self._left_rotate(current)
                    if not current.right:
                        break
                # Link current to the left tree (nodes smaller than key)
                left_tree_max.right = current
                left_tree_max = current
                current = current.right
            else:  # key == current.key
                break

        # Reassemble the tree
        left_tree_max.right = current.left
        right_tree_min.left = current.right
        current.left = dummy.right
        current.right = dummy.left
        self.root = current

    def insert(self, key):
        """
        Inserts an integer key into the tree.

        If the key already exists, it is splayed to the root.
        Otherwise, the new key is inserted and becomes the new root.
        
        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        self._splay(key)

        # If key is already present, splay has moved it to the root.
        if self.root.key == key:
            return

        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        
        self.root = new_node

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        The accessed node (or its parent if the node is not found) is
        moved to the root of the tree.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False
        self._splay(key)
        return self.root.key == key

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is found, it is deleted, and the tree is restructured.
        If the key is not found, the tree is splayed on the last accessed node.
        
        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        self._splay(key)

        # If key is not in the tree, do nothing more.
        if self.root.key != key:
            return

        # Now the node to be deleted is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
        else:
            # Splay the left subtree to bring its maximum element to its root.
            # We can splay for the key we are deleting, as it's guaranteed to be
            # larger than any key in the left subtree. This brings the max
            # element of the left subtree to its root.
            
            # Temporarily make left_subtree the main tree to splay on it.
            self.root = left_subtree
            self._splay(key)
            
            # The new root (max of left subtree) now has the right subtree attached.
            self.root.right = right_subtree