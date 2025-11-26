import sys

class SplayTree:
    """
    A self-contained Splay Tree class that implements a dictionary-like set for integers.

    This implementation includes insert, delete, and search operations. The key
    feature of a splay tree is that recently accessed elements are moved to the
    root of the tree through a series of rotations, which optimizes for access
    patterns with temporal locality.
    """

    class _Node:
        """A private helper class representing a node in the Splay Tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on the given node x."""
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
        """Performs a right rotation on the given node x."""
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
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left:
                if parent == grandparent.left:
                    # Zig-Zig case (left-left)
                    self._right_rotate(grandparent)
                    self._right_rotate(parent)
                else:
                    # Zig-Zag case (right-left)
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)
            else: # node is right child
                if parent == grandparent.right:
                    # Zig-Zig case (right-right)
                    self._left_rotate(grandparent)
                    self._left_rotate(parent)
                else:
                    # Zig-Zag case (left-right)
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the would-be parent)
        is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        last_node = None
        current = self.root
        while current:
            last_node = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found, splay the node and return True
                self._splay(current)
                return True
        
        # Key not found, splay the last accessed node if it exists
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a new key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.
        No duplicate keys are allowed.

        Args:
            key: The integer key to insert.
        """
        parent = None
        current = self.root
        
        # Find position for new node
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and return
                self._splay(current)
                return

        # Insert new node
        new_node = self._Node(key)
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

        The tree is first searched for the key, which brings the node (or its
        closest neighbor) to the root. If the key is found at the root, it is
        deleted, and its subtrees are merged.

        Args:
            key: The integer key to delete.
        """
        # Search for the key, which splays the node to the root
        if not self.search(key):
            # Key not in tree, and search has already splayed the closest node.
            return

        # At this point, the node to delete is the root, if it exists
        if not self.root or self.root.key != key:
            return

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Make left subtree the new tree
            self.root = left_subtree
            left_subtree.parent = None
            
            # Find the maximum element in the new tree (which was the left subtree)
            max_node = self.root
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to the root of the new tree
            self._splay(max_node)
            
            # Attach the original right subtree
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root