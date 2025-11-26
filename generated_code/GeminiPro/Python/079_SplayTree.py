import sys

class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.
    This tree acts as a dictionary-like set for storing unique integer keys.
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
        Performs the splay operation on node x, moving it to the root.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig case
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig case
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag case
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag case (x is left child of p, p is right child of g)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for an integer key in the tree.

        This method performs the splaying operation on the accessed node
        (or its parent if the node is not found) to move it to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_visited = None
        while node:
            last_visited = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Key not found, splay the last visited node (the parent of the
        # would-be position) to the root.
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts an integer key into the splay tree.
        If the key already exists, the node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        # Case 1: The tree is empty.
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the closest node to the key's position.
        self.search(key)

        # Case 2: The key already exists, search has splayed it to the root.
        if self.root.key == key:
            return

        # Case 3: The key does not exist. Insert a new node.
        # The root is now the closest leaf to the new key.
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
        Deletes an integer key from the splay tree.
        If the key is not in the tree, the tree is splayed based on the
        search for the key, but no node is removed.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node to be deleted (or its parent) to the root.
        self.search(key)

        # If the key is not in the tree, the root will be the closest node.
        # Do nothing if the key wasn't found.
        if self.root.key != key:
            return

        # The node to delete is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # If a left subtree exists, we find its maximum element,
            # splay it to the root of the left subtree, and then attach
            # the original right subtree as its right child.
            
            # Detach the left subtree from the original root.
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node to the top of its subtree. To do this, we
            # temporarily make the left subtree the main tree.
            self.root = left_subtree
            self._splay(max_node)
            
            # Attach the original right subtree to the new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root