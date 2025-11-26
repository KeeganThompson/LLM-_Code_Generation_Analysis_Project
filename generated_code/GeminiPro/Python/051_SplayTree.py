import sys

class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class provides a dictionary-like set interface for storing unique integers.
    It supports insert, delete, and search operations. The key feature is the
    splaying operation: whenever a key is accessed (for searching, insertion, or
    deletion), the corresponding node is moved to the root of the tree to optimize
    future accesses.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
        y = x.right
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
        
        y.left = x
        x.parent = y

    def _right_rotate(self, x):
        """Performs a right rotation on node x."""
        y = x.left
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
            
        y.right = x
        x.parent = y

    def _splay(self, node):
        """
        Performs the splay operation on a node, moving it to the root.
        This is the core operation of the Splay Tree that ensures its
        self-balancing and amortized efficiency.
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
        Searches for a key in the tree and splays the accessed node.
        
        If the key is found, its node is splayed to the root. If the key is not
        found, the last node accessed during the search (the would-be parent)
        is splayed to the root.
        
        Args:
            key: The integer key to search for.
            
        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_node = self.root
        while current:
            last_node = current
            if key == current.key:
                break
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        self._splay(last_node)
        
        return self.root and self.root.key == key

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted as in a standard BST and then the new
        node is splayed to the root.
        
        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and we are done.
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        First, the tree is searched for the key, which splays the node (if found)
        or its parent (if not found) to the root. If the key is found at the root,
        it is removed, and the remaining subtrees are joined.
        
        Args:
            key: The integer key to delete.
        """
        # The search method splays the found node or its would-be parent to the root.
        if not self.search(key):
            # Key was not found. search() has already splayed the closest node.
            return

        # Now, the node to delete is at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # Promote the left subtree
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. Join them by making the maximum element
            # of the left subtree the new root.
            
            # Detach the left subtree to operate on it independently
            self.root = left_subtree
            self.root.parent = None

            # Find the maximum node in this subtree
            max_node = self.root
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max node to the root of the subtree
            self._splay(max_node)
            
            # Now self.root is the splayed max_node. Re-attach the right subtree.
            self.root.right = right_subtree
            right_subtree.parent = self.root