class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.

    This data structure provides a dictionary-like set for integers, supporting
    efficient insert, delete, and search operations. The defining feature of a
    Splay Tree is the "splaying" operation: whenever a node is accessed, it is
    moved to the root of the tree through a sequence of rotations. This heuristic
    ensures that frequently accessed elements are quick to find, providing
    excellent amortized time complexity for all operations.
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
        Performs the splaying operation on node x, moving it to the root.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:  # Zig step
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:  # Zig-Zig (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:  # Zig-Zig (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:  # Zig-Zag (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the Splay Tree and splays the accessed node.

        If the key is found, its node is splayed to the root, and True is returned.
        If the key is not found, the last non-null node visited during the search
        is splayed to the root, and False is returned.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key exists in the tree, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_node = None
        while current:
            last_node = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the Splay Tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key does not exist, a new node is created, inserted, and then
        splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
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
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the Splay Tree.

        First, the tree is searched for the key. This brings the node (if found)
        or its would-be parent to the root. If the key was found at the root,
        it is removed, and its two subtrees are merged.

        Args:
            key (int): The integer key to delete.
        """
        # Splay the node to the root. search() handles this and returns
        # whether the key was actually found.
        if not self.search(key):
            # Key not in tree. The closest node is now at the root.
            return

        # At this point, the node to delete is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree to be the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # Promote the left subtree to be the new tree
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. Merge them.
            # Find the maximum node in the left subtree.
            left_subtree.parent = None  # Disconnect from old root
            
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max node to the root of the left subtree.
            # A common technique is to temporarily set self.root to the
            # subtree's root to reuse the main _splay method.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, max_node is the root of the merged left part
            # and has no right child. We can attach the original right subtree.
            self.root.right = right_subtree
            right_subtree.parent = self.root