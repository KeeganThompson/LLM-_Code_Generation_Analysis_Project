class SplayTree:
    """
    A complete, self-contained Python class that implements a Splay Tree.

    This class provides a dictionary-like set for storing unique integers.
    The key feature of a Splay Tree is that recently accessed elements are
    quick to access again. It achieves this by moving any accessed (searched,
    inserted, or deleted) node to the root of the tree through a series of
    rotations, an operation known as "splaying".

    The main public methods are:
    - insert(key): Adds a key to the tree.
    - delete(key): Removes a key from the tree.
    - search(key): Checks for a key and splays the tree.

    Attributes:
        root (SplayTree._Node): The root node of the tree, or None if empty.
    """

    class _Node:
        """A private inner class representing a node in the Splay Tree."""
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _splay(self, key):
        """
        Performs the top-down splay operation.

        The node with the given key (or the last node accessed if the key is
        not found) is moved to the root of the tree. This is a private helper
        method that forms the core of the Splay Tree's functionality.

        Args:
            key: The key to splay the tree around.
        """
        if not self.root:
            return

        # Dummy node simplifies linking. Its right child will form the left
        # splay tree, and its left child will form the right splay tree.
        dummy = self._Node(None)
        left_tree_tail = dummy
        right_tree_tail = dummy
        current = self.root

        while True:
            if key < current.key:
                if not current.left:
                    break
                if key < current.left.key:  # Zig-Zig (Right-Right rotation)
                    temp = current.left
                    current.left = temp.right
                    temp.right = current
                    current = temp
                    if not current.left:
                        break
                # Link to the right tree (for nodes larger than key)
                right_tree_tail.left = current
                right_tree_tail = current
                current = current.left
            elif key > current.key:
                if not current.right:
                    break
                if key > current.right.key:  # Zag-Zag (Left-Left rotation)
                    temp = current.right
                    current.right = temp.left
                    temp.left = current
                    current = temp
                    if not current.right:
                        break
                # Link to the left tree (for nodes smaller than key)
                left_tree_tail.right = current
                left_tree_tail = current
                current = current.right
            else:  # key is found
                break

        # Reassemble the tree
        left_tree_tail.right = current.left
        right_tree_tail.left = current.right
        current.left = dummy.right
        current.right = dummy.left
        self.root = current

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the tree is splayed around that key,
        but no new node is added. Otherwise, a new node with the key is
        created and inserted, becoming the new root after splaying.

        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        self._splay(key)

        # If key is already in the tree after splaying, do nothing
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
        Searches for a key in the tree and performs the splaying operation.

        This method splays the tree on the accessed node if the key is found,
        or on its would-be parent if the key is not found. This moves the
        relevant node to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False
        self._splay(key)
        return self.root.key == key

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is found, it is splayed to the root and then removed.
        The remaining subtrees are joined. If the key is not found, the tree
        is splayed around the last accessed node, but no deletion occurs.

        Args:
            key (int): The integer key to delete.
        """
        if not self.root:
            return

        self._splay(key)

        # If key is not in the tree after splaying, do nothing
        if self.root.key != key:
            return

        # Key is at the root, now perform deletion
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If no left child, the right subtree becomes the new tree
            self.root = right_subtree
        else:
            # Splay the left subtree for the key. This brings the largest
            # element (the predecessor of the deleted key) to the root of
            # the left subtree. This new root will have no right child.
            self.root = left_subtree
            self._splay(key)
            
            # Attach the original right subtree
            self.root.right = right_subtree

    def __str__(self):
        """Returns an in-order string representation of the tree's keys."""
        if not self.root:
            return "SplayTree()"
        keys = self._in_order_traversal(self.root)
        return f"SplayTree({keys})"

    def _in_order_traversal(self, node):
        """Helper for recursive in-order traversal to get keys as a list."""
        if not node:
            return []
        return (self._in_order_traversal(node.left) +
                [node.key] +
                self._in_order_traversal(node.right))