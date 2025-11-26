import sys

class SplayTree:
    """
    An implementation of a Splay Tree that acts as a dictionary-like set for integers.
    A splay tree is a self-balancing binary search tree with the additional property
    that recently accessed elements are quick to access again.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
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

    def _splay(self, node):
        """
        Performs the splay operation on a node, moving it to the root.
        """
        if not node:
            return
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
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
        self.root = node

    def search(self, key):
        """
        Searches for a key in the tree.
        
        Performs the splaying operation on the accessed node if found,
        or on the last accessed node on the search path if not found.
        
        Args:
            key: The integer key to search for.
            
        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = self.root
        while current:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found, splay it and return True
                self._splay(current)
                return True

        # Key not found. Splay the last node on the search path.
        self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, the node with that key is splayed to the root.
        If the key does not exist, it is inserted and the new node is splayed to the root.
        
        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the closest node to the root. This handles the existing key case.
        if self.search(key):
            return  # Key already exists, search has splayed it.

        # After search, the root is the closest node to where the key should be.
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None
        
        self.root.parent = new_node
        self.root = new_node

    def _find_max(self, node):
        """Finds the node with the maximum key in a subtree."""
        if not node:
            return None
        current = node
        while current.right:
            current = current.right
        return current

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        If the key is found, it is removed, and its parent or a replacement
        node is splayed. If not found, the last node on the search path is splayed.
        
        Args:
            key: The integer key to delete.
        """
        # Splay the node to the root. If not found, splay the last visited node.
        if not self.search(key):
            return  # Key not found, search already splayed the closest node.

        # At this point, the node to delete is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree to work with it independently
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree
            max_in_left = self._find_max(left_subtree)
            
            # Splay this max element to make it the root of the left subtree
            # Temporarily set the root to perform the splay within the subtree
            original_root = self.root
            self.root = left_subtree
            self._splay(max_in_left)
            
            # The new root (max_in_left) now has no right child.
            # Attach the original right subtree to it.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root
            
            # Clean up references from the deleted node (optional, for GC)
            original_root.left = None
            original_root.right = None