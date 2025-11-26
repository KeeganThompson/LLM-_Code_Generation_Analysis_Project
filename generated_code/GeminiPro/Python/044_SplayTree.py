class SplayTree:
    """
    A complete, self-contained Python class that implements a dictionary-like
    set for integers using a Splay Tree.

    The splay tree is a self-balancing binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up and removal
    in O(log n) amortized time.
    """

    class _Node:
        """A private inner class to represent a node in the splay tree."""
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _rotate_right(self, y):
        """
        Performs a right rotation around the given node y.
        Returns the new root of the rotated subtree.
        """
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def _rotate_left(self, x):
        """
        Performs a left rotation around the given node x.
        Returns the new root of the rotated subtree.
        """
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, key):
        """
        Brings the node with the given key to the root of the tree.
        If the key is not in the tree, the last accessed node is brought
        to the root. This is the core top-down splay operation.
        """
        if not self.root:
            return

        # Create a dummy node to simplify linking of left and right subtrees
        dummy = self._Node(None)
        left_tree_max = dummy
        right_tree_min = dummy
        current = self.root

        while True:
            if key < current.key:
                if not current.left:
                    break
                # Zig-Zig case: perform a rotation if the key is also in the left-left grandchild
                if key < current.left.key:
                    current = self._rotate_right(current)
                    if not current.left:
                        break
                # Link current node to the right tree (nodes larger than key)
                right_tree_min.left = current
                right_tree_min = current
                current = current.left
            elif key > current.key:
                if not current.right:
                    break
                # Zig-Zig case: perform a rotation if the key is also in the right-right grandchild
                if key > current.right.key:
                    current = self._rotate_left(current)
                    if not current.right:
                        break
                # Link current node to the left tree (nodes smaller than key)
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
        Inserts a key into the tree. If the key already exists, the tree
        is splayed on that key but the set is not modified.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree on the key to bring the closest node to the root
        self._splay(key)

        # If key is already present, do nothing further
        if self.root.key == key:
            return

        # Create the new node and split the tree
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
        Searches for a key in the tree.
        This operation splays the accessed node (or its parent if not found)
        to the root.
        Returns True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        self._splay(key)

        return self.root.key == key

    def delete(self, key):
        """
        Deletes a key from the tree. If the key is not found, the tree
        is splayed on the last accessed node and no deletion occurs.
        """
        if not self.root:
            return

        self._splay(key)

        # If key is not in the tree after splaying, do nothing
        if self.root.key != key:
            return

        # The node to delete is now at the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left child, the right child becomes the new root
            self.root = right_subtree
        else:
            # Make the left subtree the new tree
            self.root = left_subtree
            # Splay on the original key again. This will bring the largest element
            # in the left subtree (the predecessor of the deleted key) to the root.
            self._splay(key)
            # Attach the original right subtree to the new root
            self.root.right = right_subtree