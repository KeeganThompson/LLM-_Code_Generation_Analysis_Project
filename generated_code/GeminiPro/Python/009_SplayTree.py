class SplayTree:
    """
    A complete, self-contained Splay Tree class that implements a
    dictionary-like set for integers.

    The main operations (insert, delete, search) are implemented with the
    splaying step, which moves the accessed node (or its parent) to the root.
    This provides amortized O(log n) time complexity for these operations.
    """

    class _Node:
        """A private inner class representing a node in the splay tree."""
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

    def _splay(self, root, key):
        """
        Performs the top-down splay operation.

        Brings the node with the given key to the root of the tree.
        If the key is not in the tree, the last accessed node is brought to the root.
        This method returns the new root of the splayed tree.
        """
        if not root:
            return None

        # Use a dummy node to simplify linking of left and right subtrees
        dummy = self._Node(None)
        left_tree_max = right_tree_min = dummy
        current = root

        while True:
            if key < current.key:
                if not current.left:
                    break
                # Zig-Zig case (right-right)
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
                # Zig-Zig case (left-left)
                if key > current.right.key:
                    current = self._left_rotate(current)
                    if not current.right:
                        break
                # Link current to the left tree (nodes smaller than key)
                left_tree_max.right = current
                left_tree_max = current
                current = current.right
            else:  # Found key
                break
        
        # Reassemble the tree
        left_tree_max.right = current.left
        right_tree_min.left = current.right
        current.left = dummy.right
        current.right = dummy.left
        
        return current

    def insert(self, key):
        """
        Inserts a key into the splay tree.

        If the key already exists, it is simply splayed to the root.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        self.root = self._splay(self.root, key)

        # If key is already at the root, do nothing (set behavior)
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
        Searches for a key in the splay tree.

        This operation performs a splay. The node with the key (if found)
        or its would-be parent (if not found) is moved to the root.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False
        
        self.root = self._splay(self.root, key)
        
        return self.root.key == key

    def delete(self, key):
        """
        Deletes a key from the splay tree.

        If the key is not found, the tree structure may still change due to the
        splaying operation.
        """
        if not self.root:
            return

        self.root = self._splay(self.root, key)

        # If key is not in the tree (and thus not at the root after splay)
        if self.root.key != key:
            return

        # The node to delete is now the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            self.root = right_subtree
        else:
            # Splay the largest element in the left subtree to its root.
            # This makes its right child None. The largest element is the
            # predecessor of the key being deleted.
            new_root_of_left = self._splay(left_subtree, key)
            
            # Attach the original right subtree to the new root of the left subtree
            new_root_of_left.right = right_subtree
            self.root = new_root_of_left