import sys

class SplayTree:
    """
    A self-contained Python class implementing a dictionary-like set for integers
    using a Splay Tree.

    The search, insert, and delete operations are O(log n) amortized time.
    The key feature is that any accessed node (or its parent if the node is not found)
    is moved to the root of thetree via a series of rotations, a process called "splaying".
    This keeps frequently accessed elements near the top of the tree for faster access.
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
        Performs the splaying operation on a node, moving it to the root.
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
            elif node == parent.right and parent == grandparent.left:
                # Zig-Zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:
                # Zig-Zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        Performs the splaying operation on the accessed node if found,
        or on its would-be parent if not found.

        Args:
            key (int): The key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        last_node = None
        current = self.root
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

        # Key not found
        if last_node:
            # Splay the last visited node (the parent of the non-existent key)
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key (int): The key to insert.
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
                # Key already exists, splay it to the root
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

    def delete(self, key):
        """
        Deletes a key from the tree.
        First, it searches for the key, which splays the node (or its parent)
        to the root. Then, it performs the deletion.
        
        Args:
            key (int): The key to delete.
        """
        # Search for the key, which will splay it (or its parent) to the root
        if not self.search(key):
            # Key not in the tree, nothing to delete.
            # search() has already splayed the would-be parent.
            return

        # At this point, the node to delete is the root because of search()
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, promote the right subtree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        elif not right_subtree:
            # No right child, promote the left subtree
            self.root = left_subtree
            if left_subtree:
                left_subtree.parent = None
        else:
            # Both subtrees exist. Join them.
            # Find the maximum node in the left subtree.
            # This max node will become the new root.
            left_subtree.parent = None
            
            # Find the max node by traversing right
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Splay this max node to the top of the left subtree
            # Temporarily set the main root to the left subtree's root to use _splay
            self.root = left_subtree
            self._splay(max_in_left)

            # Now, self.root is max_in_left.
            # Attach the original right subtree. The new root (max_in_left)
            # is guaranteed to have no right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root

    def _inorder_helper(self, node):
        """Helper for in-order traversal."""
        if node:
            yield from self._inorder_helper(node.left)
            yield node.key
            yield from self._inorder_helper(node.right)

    def __iter__(self):
        """Returns an iterator for an in-order traversal of the keys."""
        return self._inorder_helper(self.root)

    def __str__(self):
        """Returns a string representation of the tree's keys in-order."""
        return str(list(self))