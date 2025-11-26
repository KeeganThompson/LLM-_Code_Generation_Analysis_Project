import sys

class SplayTree:
    """
    A self-contained Python class implementing a splay tree.

    This class provides a dictionary-like set for storing unique integers.
    The core operations (insert, delete, search) are implemented with the
    splaying heuristic, which moves frequently accessed elements to the root
    of the tree for faster subsequent access.

    Attributes:
        root (Node): The root node of the splay tree.
    """

    class Node:
        """A node in the splay tree."""
        def __init__(self, key: int):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
        self.root = None

    def _left_rotate(self, x: Node):
        """Performs a left rotation on the subtree rooted at x."""
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

    def _right_rotate(self, x: Node):
        """Performs a right rotation on the subtree rooted at x."""
        y = x.left
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

        y.right = x
        x.parent = y

    def _splay(self, node: Node):
        """
        Performs the splaying operation on a node, moving it to the root.

        The splaying is done through a series of rotations (Zig, Zig-Zig, Zig-Zag)
        until the node becomes the root of the tree.
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

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the root.
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
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # If key not found, splay the last accessed node
        if last_node:
            self._splay(last_node)
        
        return False

    def insert(self, key: int):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted as in a standard BST, and then the
        new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self.Node(key)
            return

        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay it and return
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Insert the new node
        new_node = self.Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key: int):
        """
        Deletes a key from the tree.

        This method first searches for the key, which brings the node (or its
        potential parent) to the root. If the key is found at the root, the
        node is removed. The remaining left and right subtrees are then joined
        by splaying the maximum element of the left subtree to its root and
        attaching the right subtree as its right child. This effectively
        makes the predecessor of the deleted key the new root.

        Args:
            key: The integer key to delete.
        """
        # Search for the key, which splays the node to the root if found.
        if not self.search(key):
            # Key not found, search has already splayed the last accessed node.
            return

        # At this point, if the key existed, it is at the root.
        # self.search() already returned and splayed.
        # So self.root.key must be equal to key.
        
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # No right subtree, the left subtree becomes the new tree.
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. Join them.
            # 1. Disconnect the left subtree.
            left_subtree.parent = None

            # 2. Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # 3. Splay this maximum node to be the root of the (temporary) left subtree.
            #    Temporarily make the left subtree the main tree to use the _splay helper.
            self.root = left_subtree
            self._splay(max_node)

            # 4. After splaying, self.root is max_node.
            #    Now, attach the original right subtree as its right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root