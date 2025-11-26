import sys

class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.

    This implementation includes methods for insertion, deletion, and searching.
    The key feature of a splay tree is that recently accessed elements are moved
    to the root of thetree to optimize for temporal locality of reference.
    """

    class Node:
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
        """Performs a left rotation on the given node x."""
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
        """Performs a right rotation on the given node x."""
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
        Performs the splay operation on the given node x, moving it to the root.
        """
        if not x:
            return
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
            else:  # Zig-Zag case (x == p.left and p == g.right)
                self._right_rotate(p)
                self._left_rotate(g)

    def insert(self, key):
        """
        Inserts a key into the tree.
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.
        """
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

        # Key is not in the tree, insert a new node
        new_node = self.Node(key)
        new_node.parent = parent

        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node to the root
        self._splay(new_node)

    def search(self, key):
        """
        Searches for a key in the tree.
        Splays the found node or the last-visited node (if not found) to the root.
        Returns True if the key is found, False otherwise.
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

        # Key not found, splay the last visited node if the tree is not empty
        if last_node:
            self._splay(last_node)
        return False

    def delete(self, key):
        """
        Deletes a key from the tree.
        This is done by first searching for the key (which splays it to the root),
        then removing it and joining the two resulting subtrees.
        """
        # Search for the key. This splays the node if found, or its parent if not.
        if not self.search(key):
            # key was not found. search() already splayed the would-be parent.
            return

        # If search returned True, the node with the key is now the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Find the maximum node in the left subtree. This will be the new root.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum node to the root of the left subtree.
            # This is done by temporarily treating the left subtree as the whole tree.
            self.root = left_subtree
            left_subtree.parent = None
            self._splay(max_node)
            
            # Now, self.root is the new root (the splayed max_node).
            # Re-attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root