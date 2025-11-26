import sys

# Set a higher recursion limit for deep trees, although this implementation is iterative.
# This is more of a safeguard for other potential recursive operations not present here.
sys.setrecursionlimit(2000)

class SplayTree:
    """
    A self-contained SplayTree class that implements a dictionary-like set for integers.

    A splay tree is a self-adjusting binary search tree with the additional property
    that recently accessed elements are quick to access again. It performs basic
    operations such as insertion, look-up and removal in O(log n) amortized time.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
        self.root = None

    def _splay(self, key):
        """
        Performs the splay operation.

        Brings the node with the given key, or the last accessed node on the search path
        if the key is not found, to the root of the tree. This is an iterative,
        top-down splay implementation.
        """
        if not self.root:
            return

        # Dummy node to simplify linking of left and right subtrees
        dummy = self._Node(None)
        left_tree_tail = dummy
        right_tree_tail = dummy

        current = self.root

        while True:
            if key < current.key:
                if not current.left:
                    break
                # Zig-Zig case (right-right)
                if key < current.left.key:
                    # Rotate right
                    temp = current.left
                    current.left = temp.right
                    temp.right = current
                    current = temp
                    if not current.left:
                        break
                # Link current node to the right tree
                right_tree_tail.left = current
                right_tree_tail = current
                current = current.left
            elif key > current.key:
                if not current.right:
                    break
                # Zig-Zig case (left-left)
                if key > current.right.key:
                    # Rotate left
                    temp = current.right
                    current.right = temp.left
                    temp.left = current
                    current = temp
                    if not current.right:
                        break
                # Link current node to the left tree
                left_tree_tail.right = current
                left_tree_tail = current
                current = current.right
            else:  # key == current.key
                break

        # Reassemble the tree
        left_tree_tail.right = current.left
        right_tree_tail.left = current.right
        current.left = dummy.right
        current.right = dummy.left
        self.root = current

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise. After the search, the node
            containing the key (if found) or the last accessed node (if not found)
            is moved to the root.
        """
        if not self.root:
            return False
        
        self._splay(key)
        
        # After splaying, the root will be the key if it exists.
        return self.root.key == key

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, it is splayed to the root. If it doesn't exist,
        it is inserted and becomes the new root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        self._splay(key)

        # If key is already in the tree, splay has brought it to the root.
        if self.root.key == key:
            return

        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
            self.root = new_node
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
            self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is found, it is deleted. The tree is re-structured by splaying.
        If the key is not found, the tree structure may change due to the splay
        operation, but no node is removed.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        self._splay(key)

        # If the key is not in the tree, do nothing after splaying.
        if self.root.key != key:
            return

        # The key to be deleted is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
        else:
            # Make the left subtree the main tree temporarily.
            self.root = left_subtree
            # Splay for the key we just deleted (or any key larger than all
            # elements in the left subtree). This brings the largest element
            # of the left subtree to its root.
            self._splay(key)
            # The new root (max element of the original left subtree) now has
            # no right child. We can attach the original right subtree here.
            self.root.right = right_subtree