import sys
from typing import Optional

class SplayTree:
    """
    Implements a Splay Tree, a self-balancing binary search tree.

    This class provides a dictionary-like set for integers with
    insert, delete, and search operations. The key feature is that
    any accessed node is moved to the root of the tree through a series
    of rotations, a process called "splaying". This ensures that
    frequently or recently accessed elements are quick to find.
    """

    class _Node:
        """A node in the Splay Tree."""
        def __init__(self, key: int, parent: Optional['SplayTree._Node'] = None):
            self.key = key
            self.parent = parent
            self.left: Optional['SplayTree._Node'] = None
            self.right: Optional['SplayTree._Node'] = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root: Optional[SplayTree._Node] = None

    def _left_rotate(self, x: _Node):
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

    def _right_rotate(self, x: _Node):
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

    def _splay(self, node: _Node):
        """
        Performs the splay operation on a node, moving it to the root.
        """
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
            elif node == parent.left and parent == grandparent.right:  # Zig-Zag case
                self._right_rotate(parent)
                self._left_rotate(grandparent)
            else:  # Zig-Zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree.
        
        The accessed node (if found) or its parent (if the key is not found)
        is splayed to become the new root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_node = None
        while current:
            last_node = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found, splay the node and return
                self._splay(current)
                return True

        # Key not found, splay the last visited node (the would-be parent)
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key: int):
        """
        Inserts a key into the tree.
        
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is then splayed
        to the root.

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
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and return
                self._splay(current)
                return

        # Insert the new node
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key: int):
        """
        Deletes a key from the tree.
        
        This method first searches for the key, which splays the accessed
        node (or its parent) to the root. If the key is found at the root,
        it is removed, and its two subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # search() will splay the node with the key (or its parent) to the root
        self.search(key)

        # If the key is not at the root after splaying, it wasn't in the tree
        if self.root.key != key:
            return

        # The node to delete is now the root.
        # Split the tree into two subtrees: L < key and R > key
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree to be the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # Promote the left subtree to be the new tree
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Join the two subtrees.
            # Detach the left subtree to operate on it
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum node to the root of the (temporary) left subtree.
            self.root = left_subtree
            self._splay(max_node)

            # Attach the original right subtree. After splaying, the new root
            # (max_node) has no right child, so we can attach it there.
            self.root.right = right_subtree
            right_subtree.parent = self.root