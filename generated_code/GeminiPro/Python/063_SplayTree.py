import sys

class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.

    This class provides a dictionary-like set for storing unique integer keys.
    It supports insertion, deletion, and searching operations. A key feature
    is the splaying operation, which moves accessed elements to the root of
    the tree to optimize for future accesses.
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

    def insert(self, key):
        """
        Inserts a key into the Splay Tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted as in a standard BST, and the new
        node is then splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        if self.root is None:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current is not None:
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

    def search(self, key):
        """
        Searches for a key in the Splay Tree.

        If the key is found, the corresponding node is splayed to the root
        and the method returns True. If the key is not found, the last
        accessed node (the would-be parent) is splayed to the root and
        the method returns False.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        current = self.root
        last_visited = None
        while current is not None:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                self._splay(current)
                return True
        
        # Key not found, splay the last visited node (parent)
        if last_visited:
            self._splay(last_visited)
        return False

    def delete(self, key):
        """
        Deletes a key from the Splay Tree.

        The node with the given key is first splayed to the root. If it exists,
        it is removed. The tree is then reformed by joining the left and right
        subtrees. The largest element of the left subtree becomes the new root.

        Args:
            key (int): The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node with the key (or its parent) to the root
        self.search(key)

        # If the key is not at the root, it wasn't in the tree
        if self.root.key != key:
            return

        # Now the node to delete is the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if left_subtree is None:
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif right_subtree is None:
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree from the old root
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Temporarily make the left subtree the main tree to splay within it
            temp_root = self.root
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, max_node is the new root of the (modified) left subtree.
            # It has no right child. We attach the original right subtree here.
            self.root.right = right_subtree
            right_subtree.parent = self.root

    # ----------------- Private Helper Methods -----------------

    def _left_rotate(self, x):
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
            y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        if y:
            y.right = x
        x.parent = y

    def _splay(self, node):
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if grandparent is None:
                # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            else:
                if node == parent.left:
                    if parent == grandparent.left:
                        # Zig-Zig case (left-left)
                        self._right_rotate(grandparent)
                        self._right_rotate(parent)
                    else:
                        # Zig-Zag case (right-left)
                        self._right_rotate(parent)
                        self._left_rotate(grandparent)
                else:
                    if parent == grandparent.right:
                        # Zig-Zig case (right-right)
                        self._left_rotate(grandparent)
                        self._left_rotate(parent)
                    else:
                        # Zig-Zag case (left-right)
                        self._left_rotate(parent)
                        self._right_rotate(grandparent)