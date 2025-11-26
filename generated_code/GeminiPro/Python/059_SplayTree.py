class SplayTree:
    """
    A complete, self-contained Python class that implements a Splay Tree.

    This class provides a dictionary-like set interface for storing unique integer keys.
    It supports the essential methods: insert(key), delete(key), and search(key).
    The splay operation is performed on accessed nodes to move them to the root,
    optimizing for frequent access to the same elements.
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
        Splays the node x to the root of the tree.
        This operation moves the node x to the root through a series of rotations.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case
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
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last non-null node accessed during the
        search is splayed to the root.

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
        
        if last_node:
            self._splay(last_node)
        
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        Otherwise, a new node is created, inserted as in a regular BST, and
        then splayed to the root.

        Args:
            key: The integer key to insert.
        """
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay it to the root and we're done
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        new_node = self._Node(key)
        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
            
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The node with the given key is first splayed to the root. Then, it is
        removed by joining its left and right subtrees. To join, the maximum
        element of the left subtree is splayed to its root and then the right
        subtree is attached as its right child.

        Args:
            key: The integer key to delete.
        """
        if not self.search(key):
            # Key not found, nothing to delete.
            # search() has already splayed the closest node.
            return
            
        # After search, the node to be deleted is at the root.
        # This is guaranteed if the key was found.
        left_subtree = self.root.left
        right_subtree = self.root.right
        
        if not left_subtree:
            # No left subtree, so the right subtree becomes the new tree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect left subtree to treat it as its own tree
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node to the root of its subtree.
            # We can do this by temporarily setting self.root to the left subtree's root.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, self.root is max_node. We reattach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root