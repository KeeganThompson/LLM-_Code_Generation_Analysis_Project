import sys

class SplayTree:
    """
    A self-contained Python class that implements a Splay Tree.

    This class provides a dictionary-like set for storing unique integer keys.
    It supports insertion, deletion, and searching operations. The key feature
    of a splay tree is that recently accessed elements are moved to the root
    of the tree to optimize for temporal locality, providing amortized
    O(log n) time complexity for its main operations.
    """

    class _Node:
        """A node in the Splay Tree."""
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

    def _splay(self, x):
        """
        Performs the splaying operation on node x, moving it to the root.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:  # Zig-Zig case
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:  # Zig-Zig case
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            else:  # Zig-Zag case
                if x == parent.right and parent == grandparent.left:
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)
                else: # x == parent.left and parent == grandparent.right
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        Performs the splaying operation on the accessed node if the key is found,
        or on the last accessed node (its would-be parent) if the key is not found.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key found, splay the node and return True
                self._splay(node)
                return True
        
        # Key not found. Splay the last accessed node (if any)
        if last_node:
            self._splay(last_node)
            
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and then the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        node = self.root
        parent = None
        
        # Traverse to find the insertion point or an existing key
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key already exists, splay it and we are done
                self._splay(node)
                return
        
        # Key is not in the tree, create a new node
        new_node = self._Node(key)
        new_node.parent = parent
        
        if not parent:
            # The tree was empty
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

        If the key is found, it is deleted. The tree structure is maintained
        by splaying and joining subtrees. If the key is not found, the tree
        is splayed on the last accessed node but no deletion occurs.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node with the key (or its parent) to the root
        self.search(key)
        
        # After search, if the key exists, it's at the root.
        # If not, the root is the closest element, so we don't delete.
        if self.root.key != key:
            return

        # The node to delete is now at the root
        root_to_delete = self.root
        left_subtree = root_to_delete.left
        right_subtree = root_to_delete.right

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
            # Both subtrees exist. Join them.
            # Disconnect left subtree from the old root
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node to be the root of the (now modified) left subtree
            # Temporarily set self.root to perform the splay within the subtree
            self.root = left_subtree
            self._splay(max_node) # Now self.root is max_node
            
            # Attach the original right subtree to the new root
            self.root.right = right_subtree
            right_subtree.parent = self.root