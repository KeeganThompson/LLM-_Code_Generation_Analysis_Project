class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class implements a dictionary-like set for integer keys. Splay trees
    are self-balancing binary search trees with the property that recently
    accessed elements are quick to access again. Operations like insert, delete,
    and search have an amortized time complexity of O(log n).

    The core of this tree is the 'splay' operation, which moves a specific
    node to the root of the tree through a series of rotations. This is
    performed on every search, insert, and delete operation.
    """

    class _Node:
        """A private class representing a node in the splay tree."""
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _right_rotate(self, x):
        """Performs a right rotation on the subtree rooted at x."""
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        """Performs a left rotation on the subtree rooted at x."""
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, key):
        """
        Performs the top-down splay operation.

        This method brings the node with the given key to the root. If the key
        is not in the tree, the last accessed node (the would-be parent) is
        brought to the root. This method modifies `self.root` directly.
        """
        if not self.root:
            return

        # Use a dummy node to simplify linking of left and right subtrees
        dummy = self._Node(None)
        left_tree = dummy
        right_tree = dummy
        current = self.root

        while True:
            if key < current.key:
                if not current.left:
                    break
                # Zig-Zig case (right rotation)
                if key < current.left.key:
                    current = self._right_rotate(current)
                    if not current.left:
                        break
                # Link current node to the right tree
                right_tree.left = current
                right_tree = current
                current = current.left
            elif key > current.key:
                if not current.right:
                    break
                # Zig-Zig case (left rotation)
                if key > current.right.key:
                    current = self._left_rotate(current)
                    if not current.right:
                        break
                # Link current node to the left tree
                left_tree.right = current
                left_tree = current
                current = current.right
            else:  # Key is found
                break

        # Reassemble the tree
        left_tree.right = current.left
        right_tree.left = current.right
        current.left = dummy.right
        current.right = dummy.left
        
        self.root = current

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node is splayed to the root. If the key
        is new, it is inserted and becomes the new root.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree to bring the closest node to the root
        self._splay(key)

        # If key is already at the root, insertion is complete
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

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is not found, the tree is splayed based on the search path,
        but no node is removed.
        """
        if not self.root:
            return

        # Splay the tree to bring the node to delete (if it exists) to the root
        self._splay(key)

        # If the key is not in the tree, do nothing
        if self.root.key != key:
            return

        # At this point, the node to delete is the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree
            self.root = right_subtree
        else:
            # The left subtree becomes the temporary root
            self.root = left_subtree
            # Splay the temporary tree for the key we are deleting. This will
            # bring the maximum element of the left subtree to its root.
            self._splay(key)
            # The new root (max of left subtree) has no right child, so we
            # can attach the original right subtree there.
            self.root.right = right_subtree

    def search(self, key):
        """
        Searches for a key in the tree.

        This operation splays the found node (or its would-be parent if not
        found) to the root of the tree.
        
        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False
            
        self._splay(key)
        
        # After splaying, the key will be at the root if it exists
        return self.root.key == key