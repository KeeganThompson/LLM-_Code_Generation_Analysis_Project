import sys

class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.
    
    Splay trees are self-balancing binary search trees with the additional property
    that recently accessed elements are quick to access again. It achieves this
    by moving any accessed node to the root of the tree through a series of
    rotations in an operation called "splaying".

    This implementation includes the following methods:
    - insert(key): Adds an integer key to the set.
    - delete(key): Removes an integer key from the set.
    - search(key): Checks for the existence of a key and splays the accessed node.
    """

    class _Node:
        """A private inner class to represent a node in the Splay Tree."""
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
        """
        Performs the splaying operation on node x, moving it to the root.
        
        The splaying operation consists of a sequence of tree rotations:
        - Zig: If the parent is the root.
        - Zig-Zig: If the node and its parent are both left/right children.
        - Zig-Zag: If the node is a right child and parent is a left child (or vice versa).
        """
        if not x:
            return
            
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
            elif x == parent.right and parent == grandparent.left:  # Zig-Zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (x is left child, parent is right child)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        Performs the splaying operation on the accessed node if the key is found,
        or on the last accessed node (the parent of the potential location) if
        the key is not found.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        last_visited_node = None
        current = self.root
        while current:
            last_visited_node = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # If key was not found, splay the last non-null node visited.
        if last_visited_node:
            self._splay(last_visited_node)
        
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Search for the key. This splays the tree, bringing the closest node to the root.
        self.search(key)

        # If key already exists, search would have splayed it and we're done.
        if self.root.key == key:
            return

        # Otherwise, insert the new key and make it the new root.
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
            self.root.parent = new_node
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None
            self.root.parent = new_node
        
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.

        The parent of the deleted node (or the node that replaced it) is splayed
        to the root.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Search for the key, which splays the node (if found) to the root.
        self.search(key)

        # If key is not in the tree, the root will be the closest node.
        # We only proceed with deletion if the key is actually at the root.
        if self.root.key != key:
            return

        # The node to delete is now the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree to be the new root.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # Promote the left subtree to be the new root.
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Join the left and right subtrees.
            # 1. Detach the left subtree.
            left_subtree.parent = None

            # 2. Find the maximum key in the left subtree.
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right

            # 3. Splay this maximum node to the root of the left subtree.
            #    After this, it will have no right child.
            #    We temporarily set self.root to perform splay on the subtree.
            self.root = left_subtree
            self._splay(max_in_left)

            # 4. Attach the original right subtree as the right child of the new root.
            self.root.right = right_subtree
            right_subtree.parent = self.root