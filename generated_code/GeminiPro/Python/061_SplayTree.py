class SplayTree:
    """
    An implementation of a dictionary-like set for integers using a Splay Tree.

    This class supports insert, delete, and search operations. The key feature
    of a splay tree is that any accessed node is moved to the root of the tree
    through a series of rotations, which provides amortized O(log n) time
    complexity for these operations.
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
        if not x:
            return
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:  # Zig-Zig
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:  # Zig-Zig
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:  # Zig-Zag
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag (x is left child, parent is right child)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root.
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
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return True
        
        # Key not found, splay the last accessed node if it exists
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
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key already exists, splay it and return
                self._splay(node)
                return

        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The standard splay tree deletion algorithm is used (split and join).
        First, the key is searched for, which brings the node (if it exists)
        or its would-be parent to the root. If the key exists, the node is
        removed, and its two subtrees are merged.

        Args:
            key: The integer key to delete.
        """
        # Search will splay the node if found, or the parent if not found.
        if not self.search(key):
            # Key not in tree. The would-be parent is now the root. Nothing to delete.
            return

        # At this point, the node to delete is the root because search() splayed it.
        z = self.root
        
        left_subtree = z.left
        right_subtree = z.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree from the root.
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element. It will become the new root of the
            # combined tree. We do this by temporarily setting the root to
            # the left subtree and then splaying within it.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, the new root (max_node) has no right child.
            # We can now attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root