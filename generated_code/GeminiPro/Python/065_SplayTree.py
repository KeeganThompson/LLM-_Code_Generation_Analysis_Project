import sys

class SplayTree:
    """
    An implementation of a Splay Tree.

    This class provides a dictionary-like set for integers, supporting
    insert, delete, and search operations. The key feature is that any
    accessed (searched, inserted, or deleted) node is moved to the root
    of the tree through a series of rotations, a process called "splaying".
    This self-adjusting property provides good amortized performance for
    various access patterns.
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
        Performs the splaying operation on a node, moving it to the root.
        """
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

    def insert(self, key):
        """
        Inserts an integer key into the tree.
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then the new node is splayed.

        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and return
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Insert the new node as a leaf
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root
        self._splay(new_node)

    def search(self, key):
        """
        Searches for a key in the tree.
        Splays the found node to the root. If the key is not found, the last
        accessed node (the would-be parent) is splayed to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = None
        while current:
            last_visited = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
        return False

    def delete(self, key):
        """
        Deletes a key from the tree.
        The tree is first splayed on the key. If the key is found, it is
        removed, and its two subtrees are joined.

        Args:
            key (int): The integer key to delete.
        """
        if not self.root:
            return

        # Splay the tree on the key. This brings the node to delete (if it exists)
        # or its would-be parent to the root.
        found = self.search(key)

        # If the key is not at the root after splaying, it was not in the tree.
        if not found or self.root.key != key:
            return

        # The node to delete is now the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # If there's no right subtree, the left subtree becomes the new tree.
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. Join them.
            # 1. Find the maximum node in the left subtree.
            left_subtree.parent = None # Temporarily detach
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # 2. Splay this max node to the root of the left subtree.
            #    This makes it the new root of the combined tree and ensures
            #    it has no right child, ready to adopt the right_subtree.
            self.root = left_subtree # Temporarily set root for splaying context
            self._splay(max_node)
            
            # 3. Attach the original right subtree as the right child of the new root.
            self.root.right = right_subtree
            right_subtree.parent = self.root