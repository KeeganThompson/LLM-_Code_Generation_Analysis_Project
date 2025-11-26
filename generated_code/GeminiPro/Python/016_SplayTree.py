class SplayTree:
    """
    An implementation of a Splay Tree, a self-balancing binary search tree.
    This class provides a dictionary-like set for storing unique integer keys.
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

    def _splay(self, node):
        """
        Splays the given node to the root of the tree through a series of rotations.
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
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig case
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig case
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (node is left child, parent is right child)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

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
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:  # Key found
                self._splay(node)
                return True

        # Key not found, splay the last visited node if it exists
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key is not already in the tree, it is inserted and the new node
        is splayed to the root. If the key already exists, the existing node
        is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        parent = None
        current = self.root
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
        
        After deletion, the parent of the removed node is splayed.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. This will splay the node (if found) or its
        # parent (if not found) to the root.
        if not self.search(key):
            # Key is not in the tree, nothing to delete.
            # search() has already splayed the appropriate node.
            return

        # At this point, the node to be deleted is at the root because search(key)
        # returned True, and self.root.key == key.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # The left subtree becomes the main part of the new tree.
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max element to the root of the (now detached) left subtree.
            # This is done by temporarily setting self.root to the left_subtree's root
            # and then calling the standard _splay method.
            self.root = left_subtree
            self._splay(max_node)
            # After splaying, self.root is max_node, which becomes the new root of the
            # final combined tree.
            
            # Attach the original right subtree to the new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root