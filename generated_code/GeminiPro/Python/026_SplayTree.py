import sys

class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree that acts as a
    dictionary-like set for integers.

    Splay trees are self-balancing binary search trees with the additional
    property that recently accessed elements are quick to access again. This
    is achieved by moving any accessed node to the root of the tree through
    a series of rotations, an operation called "splaying".

    Attributes:
        root (_Node): The root node of the splay tree.
    """

    class _Node:
        """A private helper class representing a node in the Splay Tree."""
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
        Splays the given node to the root of the tree using a series of
        zig, zig-zig, and zig-zag rotations.
        """
        if not node:
            return

        while node.parent:
            p = node.parent
            g = p.parent
            if not g:  # Zig step (parent is root)
                if node == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif node == p.left and p == g.left:  # Zig-Zig (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif node == p.right and p == g.right:  # Zig-Zig (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif node == p.right and p == g.left:  # Zig-Zag (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag (right-left)
                self._right_rotate(p)
                self._left_rotate(g)
        
        self.root = node

    def insert(self, key):
        """
        Inserts a key into the Splay Tree. If the key already exists,
        the existing node is splayed to the root. Otherwise, a new node
        is created, inserted, and then splayed to the root.
        """
        parent = None
        current = self.root
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

        # Key does not exist, create and insert a new node
        new_node = self._Node(key)
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
        If the key is found, the corresponding node is splayed to the root and
        True is returned. If the key is not found, the last accessed node
        (the parent where the key would be) is splayed to the root and
        False is returned.
        """
        node = self.root
        last_visited = None
        while node is not None:
            last_visited = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key found, splay the node
                self._splay(node)
                return True
        
        # Key not found, splay the last visited node (if any)
        if last_visited:
            self._splay(last_visited)
        
        return False

    def delete(self, key):
        """
        Deletes a key from the Splay Tree.
        First, it searches for the key, which brings the node (or its closest
        relative) to the root. If the key is found at the root, it is removed
        by splitting the tree into its left and right subtrees, and then joining
        them. The join operation involves splaying the maximum element of the
        left subtree to its root and then attaching the right subtree.
        """
        # Search for the key. This splays the node to the root if found.
        if not self.search(key):
            # Key is not in the tree, nothing to delete.
            # search() has already splayed the closest node.
            return

        # After search, if the key was found, it's at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Isolate the left subtree to perform operations on it.
            left_subtree.parent = None

            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum node to the root of the left subtree.
            # We can do this by temporarily setting the tree's root to the
            # left subtree's root and then using the existing _splay method.
            self.root = left_subtree
            self._splay(max_node)

            # After splaying, self.root is the new root of the combined tree.
            # Re-attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root