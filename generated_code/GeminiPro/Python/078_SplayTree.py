class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class provides a dictionary-like set for storing unique integers.
    It supports insert, delete, and search operations, all of which leverage
    the splaying mechanism to maintain amortized logarithmic time complexity.
    """

    class _Node:
        """A private class representing a node in the Splay Tree."""
        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty Splay Tree."""
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
        Splays the given node to the root of the tree.
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
            elif node == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            else:
                # Zig-Zag case
                if node == parent.right and parent == grandparent.left:
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)
                else: # node == parent.left and parent == grandparent.right
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        Performs the splaying operation on the accessed node if found,
        or on its would-be parent if not found.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise. After the call,
            the splayed node will be the new root of the tree.
        """
        current = self.root
        last_node = None
        while current:
            last_node = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # If key was not found, splay the last accessed node
        if last_node:
            self._splay(last_node)
        
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key does not exist, a new node is created, inserted, and then
        splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the closest node to the root
        self.search(key)
        
        # If key is already in the tree, search would have splayed it
        if self.root.key == key:
            return

        # Create the new node and split the tree
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if new_node.left:
                new_node.left.parent = new_node
            self.root.parent = new_node
            self.root.left = None
        else: # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if new_node.right:
                new_node.right.parent = new_node
            self.root.parent = new_node
            self.root.right = None
        
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is found, it is removed, and the tree is re-structured.
        The operation involves splaying the node to the root, removing it,
        and then joining the two resulting subtrees.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node with the given key to the root
        self.search(key)

        # If the key is not at the root after splaying, it doesn't exist
        if self.root.key != key:
            return

        # Now, the node to delete is the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree to work on it
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum node to the root of the left subtree
            # We can temporarily set self.root to the left subtree's root
            # to reuse the _splay method.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, the new root (max_node) has no right child.
            # We can now attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root