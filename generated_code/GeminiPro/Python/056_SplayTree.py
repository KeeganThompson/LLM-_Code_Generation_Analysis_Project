import sys

class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.

    This implementation includes insert, delete, and search operations. The key
    feature of a splay tree is that recently accessed elements are moved to the
    root of the tree to optimize for temporal locality, providing amortized
    O(log n) time complexity for its operations.
    """

    class _Node:
        """A node in the splay tree."""
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

    def _splay(self, x):
        """
        Splays the node x to the root of the tree.
        This operation moves the node x to the root position through a series
        of rotations.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-zig case (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-zig case (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-zag case (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-zag case (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        If the key is found, the corresponding node is splayed to the root and
        True is returned. If the key is not found, the last accessed node (the
        would-be parent) is splayed to the root and False is returned.
        
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
        
        # If key not found, splay the last visited node.
        if last_visited:
            self._splay(last_visited)
            
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key is not already in the tree, it is inserted and the new node
        is splayed to the root. If the key already exists, the existing node
        is splayed to the root.
        
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
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        First, the key is searched. If found, it's splayed to the root and then
        removed by joining its two subtrees. If not found, the last accessed
        node is splayed, and the tree remains unchanged.
        
        Args:
            key (int): The integer key to delete.
        """
        if not self.search(key):
            # Key not in tree. search() has already splayed the closest node.
            return

        # After search, the node to delete is at the root
        z = self.root
        left_subtree = z.left
        right_subtree = z.right

        if not left_subtree:
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree to find its maximum element
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            new_root = left_subtree
            while new_root.right:
                new_root = new_root.right
            
            # Splay this maximum node to the root of the left subtree
            # Since left_subtree is now a disconnected component, this splay
            # will make new_root its root.
            self.root = left_subtree # Temporarily set root for splay context
            self._splay(new_root)

            # Join the right subtree to the new root of the left subtree
            new_root.right = right_subtree
            right_subtree.parent = new_root
            self.root = new_root