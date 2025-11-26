import sys

# It's good practice to increase recursion limit for tree structures,
# though this implementation is iterative to avoid it.
# sys.setrecursionlimit(10**6)

class SplayTree:
    """
    A self-contained Python class that implements a Splay Tree.
    
    This class provides a dictionary-like set for storing unique integer keys.
    It includes insert, delete, and search operations. The key feature is the
    splaying operation: whenever a key is accessed (searched, inserted, or
    deleted), the corresponding node is moved to the root of the tree to
    optimize future accesses for that key.
    """

    class _Node:
        """A private inner class representing a node in the Splay Tree."""
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

    def _splay(self, x):
        """
        Performs the splaying operation on node x, moving it to the root.
        This is the core operation that gives the Splay Tree its self-balancing
        and self-optimizing properties.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case (parent is root)
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig case (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig case (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag case (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag case (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        Performs the splaying operation on the accessed node if found. If the
        node is not found, its would-be parent (the last node visited) is
        splayed to the root.

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

        # Key not found, splay the last visited node (the would-be parent)
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted as in a standard BST, and then the
        new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay it and we're done
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Create the new node
        new_node = self._Node(key, parent)

        # Insert the new node into the tree
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        First, it searches for the key, which splays the node to the root if
        found. If the key is not found, its parent is splayed and the operation
        ends. If the key is found and splayed, it is removed, and its two
        subtrees are merged.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. This also splays the node (or its parent) to the root.
        if not self.search(key):
            # Key was not found. search() already splayed the would-be parent.
            # There's nothing to delete.
            return

        # After a successful search(), the node with the key is at the root.
        node_to_delete = self.root
        
        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree from the old root.
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree.
            max_node_in_left = left_subtree
            while max_node_in_left.right:
                max_node_in_left = max_node_in_left.right
            
            # Splay this maximum node to the root of the (temporary) left subtree.
            # This is a common technique: temporarily treat the subtree as the
            # whole tree to reuse the _splay method.
            self.root = left_subtree
            self._splay(max_node_in_left)
            
            # After splaying, self.root is the new root of the merged tree.
            # This new root (max_node_in_left) has no right child.
            # Attach the original right subtree as its right child.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root