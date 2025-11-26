import sys

class SplayTree:
    """
    A complete, self-contained Splay Tree class that implements a
    dictionary-like set for integers.

    The splay tree is a self-adjusting binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up and removal
    in O(log n) amortized time.
    """

    class _Node:
        """A private node class for the Splay Tree."""
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
        Inserts a key into the tree.
        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay this node and return
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Insert the new node at the found position
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        The node to be deleted is first splayed to the root. Then, its left
        and right subtrees are merged. The root of the merged tree is the
        in-order predecessor of the deleted node. If the key is not found,
        the last-accessed node on the search path is splayed.
        """
        # Search for the key. This will splay the node (or its parent) to the root.
        if not self.search(key):
            # Key was not in the tree. search() already splayed the closest node.
            return

        # After search, if the key was found, it is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum node to the root of the left subtree.
            # We can do this by temporarily treating the left subtree as the main tree.
            self.root = left_subtree
            left_subtree.parent = None
            self._splay(max_node)

            # After splaying, `self.root` is `max_node`. It has no right child.
            # We can now attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root

    def search(self, key):
        """
        Searches for a key in the tree.
        Performs the splaying operation on the accessed node if found. If not
        found, the last non-null node on the search path is splayed.
        
        Returns:
            True if the key is found, False otherwise.
        """
        last_node = None
        current = self.root
        while current:
            last_node = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Key not found. Splay the last accessed node if the tree is not empty.
        if last_node:
            self._splay(last_node)

        return False

    # --- Private Helper Methods ---

    def _splay(self, node):
        """
        Performs the splay operation on a given node, moving it to the root
        through a series of rotations.
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