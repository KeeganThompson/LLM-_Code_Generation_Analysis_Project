import sys

class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.

    This class provides a dictionary-like set for storing unique integers.
    It supports insert, delete, and search operations. The key feature is
    the splaying operation, which moves frequently accessed elements to the
    root of the tree to optimize performance for certain access patterns.

    Attributes:
        root (Node): The root node of the splay tree.
    """

    class Node:
        """A node in the splay tree."""
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
        self.root = None

    def _right_rotate(self, y):
        """Performs a right rotation on the subtree rooted at y."""
        x = y.left
        y.left = x.right
        x.right = y
        return x

    def _left_rotate(self, x):
        """Performs a left rotation on the subtree rooted at x."""
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, key):
        """
        Performs the splay operation.

        Searches for the given key and brings the accessed node (or the last
        node on the search path) to the root of the tree.
        This is a top-down splay implementation.
        """
        if not self.root:
            return

        # Use a dummy node to simplify linking
        dummy = self.Node(None)
        left_tree, right_tree = dummy, dummy
        current = self.root

        while True:
            if key < current.key:
                if not current.left:
                    break
                if key < current.left.key:
                    # Zig-Zig (left-left)
                    current = self._right_rotate(current)
                    if not current.left:
                        break
                # Link current's root to the right tree
                right_tree.left = current
                right_tree = current
                current = current.left
            elif key > current.key:
                if not current.right:
                    break
                if key > current.right.key:
                    # Zig-Zig (right-right)
                    current = self._left_rotate(current)
                    if not current.right:
                        break
                # Link current's root to the left tree
                left_tree.right = current
                left_tree = current
                current = current.right
            else:
                # Key found
                break

        # Reassemble the tree
        left_tree.right = current.left
        right_tree.left = current.right
        current.left = dummy.right
        current.right = dummy.left
        self.root = current

    def insert(self, key):
        """
        Inserts an integer key into the tree.

        If the key already exists, it is splayed to the root. If it doesn't
        exist, it is inserted and then becomes the new root.
        
        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self.Node(key)
            return

        self._splay(key)

        # If key is already present, splaying has moved it to the root.
        if self.root.key == key:
            return

        new_node = self.Node(key)
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

        Performs the splaying operation on the accessed node (or its parent
        if the node is not found) to move it to the root.

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

        The parent of the deleted node (or the last accessed node if the key
        is not found) is splayed to the root.

        Args:
            key (int): The integer key to delete.
        """
        if not self.root:
            return

        self._splay(key)

        # If key is not in the tree, splaying has moved the would-be parent to root.
        if self.root.key != key:
            return

        # Key is at the root, now we need to delete it.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            self.root = right_subtree
        else:
            # The new root will be the maximum element in the left subtree.
            # We splay for the key we are deleting in the left subtree. Since all
            # keys there are smaller, this will bring the max element to the top.
            self.root = left_subtree
            self._splay(key)
            
            # The new root (max of left subtree) is guaranteed to have no right child.
            # Attach the original right subtree there.
            self.root.right = right_subtree