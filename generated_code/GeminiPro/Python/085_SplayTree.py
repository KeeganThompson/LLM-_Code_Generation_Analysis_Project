import sys

class SplayTree:
    """
    An implementation of a Splay Tree.

    This class provides a dictionary-like set for integers, supporting
    insert, delete, and search operations. The key feature is the splaying
    operation: whenever a key is accessed (searched, inserted, or deleted),
    the node containing that key (or its parent/successor if the key is not found)
    is moved to the root of the tree. This self-optimizing behavior provides
    amortized O(log n) time complexity for all operations.
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
        """Performs a left rotation around node x."""
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
        """Performs a right rotation around node x."""
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
        Performs the splaying operation on a node, moving it to the root.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig step
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

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root
        and the method returns True. If the key is not found, the last
        accessed node (the would-be parent) is splayed to the root and
        the method returns False.

        Args:
            key (int): The key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
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

        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key is not already in the tree, it is inserted and the new
        node is splayed to the root. If the key already exists, the existing
        node is splayed to the root.

        Args:
            key (int): The key to insert.
        """
        parent_node = None
        current_node = self.root
        while current_node:
            parent_node = current_node
            if key < current_node.key:
                current_node = current_node.left
            elif key > current_node.key:
                current_node = current_node.right
            else:
                # Key already exists, splay it and return
                self._splay(current_node)
                return

        new_node = self._Node(key)
        new_node.parent = parent_node

        if not parent_node:
            self.root = new_node
        elif key < parent_node.key:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The node containing the key is first splayed to the root and then
        removed. If the key is not found, the last accessed node is splayed
        to the root.

        Args:
            key (int): The key to delete.
        """
        # First, search for the key. This splays the node (if found)
        # or its would-be parent (if not found) to the root.
        if not self.search(key):
            # Key was not in the tree. search() already splayed the parent.
            return

        # At this point, the node to delete is the root, and we know it exists.
        assert self.root.key == key

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # The right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum node to be the root of the left subtree.
            # We can do this by temporarily making the left subtree the main tree.
            original_root = self.root
            self.root = left_subtree
            self._splay(max_node)
            
            # Now, self.root is the splayed max_node.
            # Re-attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root