class SplayTree:
    """
    A self-contained Python class that implements a dictionary-like set for integers
    using a Splay Tree.

    This class supports `insert`, `delete`, and `search` operations. The key
    feature of a splay tree is that any accessed node (or its parent, if the
    node is not found) is moved to the root of the tree through a series of
    rotations. This property provides good amortized performance for many
    sequences of operations.
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
        """Performs a left rotation on the given node x."""
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
        """Performs a right rotation on the given node x."""
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
        Performs the splay operation on node x, moving it to the root.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:
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
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Key not found, splay the last visited node if the tree is not empty.
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        parent = None
        current = self.root
        
        # Find the position for the new node or an existing node with the same key
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and return
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Insert the new node
        new_node = self._Node(key)
        new_node.parent = parent
        
        if not parent:
            self.root = new_node  # Tree was empty
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
            
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The tree is first searched for the key, which brings the node (or its
        would-be parent) to the root. If the key is found, it is removed, and
        the tree is re-joined.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. If found, it will be splayed to the root.
        # If not found, its parent will be splayed, and we do nothing.
        if not self.search(key):
            return

        # At this point, the node to delete is the root
        z = self.root
        left_subtree = z.left
        right_subtree = z.right

        if not left_subtree:
            # No left subtree, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree from the old root
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            current = left_subtree
            while current.right:
                current = current.right
            max_node_in_left = current
            
            # Splay this max node to become the root of the left subtree
            # We achieve this by temporarily setting self.root and using _splay
            self.root = left_subtree
            self._splay(max_node_in_left)
            
            # After splaying, self.root is the new root of the combined tree.
            # Its right child is guaranteed to be None. Attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root