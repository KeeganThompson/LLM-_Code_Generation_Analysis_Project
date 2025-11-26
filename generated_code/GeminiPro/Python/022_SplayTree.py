class SplayTree:
    """
    A self-contained Python class implementing a splay tree.
    This tree functions as a dictionary-like set for storing unique integers.
    The main operations (insert, delete, search) are implemented with the
    characteristic splaying operation to maintain amortized logarithmic time
    complexity.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty splay tree."""
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
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
            if not grandparent:  # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:  # Zig-Zig case
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:  # Zig-Zig case
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            else:  # Zig-Zag case
                if x == parent.right and parent == grandparent.left:
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)
                else: # x == parent.left and parent == grandparent.right
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        If the key is found, the corresponding node is splayed to the root and
        True is returned.
        
        If the key is not found, the last accessed node (the would-be parent)
        is splayed to the root and False is returned.
        
        Returns:
            bool: True if the key is found, False otherwise.
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
        
        # Key not found, splay the last accessed node
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.
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
        
        # Insert new node
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        The search for the key will cause a splay operation. If the key is
        found, it is removed, and its subtrees are merged.
        """
        # First, search for the key. This will splay it to the root if found.
        if not self.search(key):
            # Key not in the tree, nothing to delete.
            # search() already splayed the closest node.
            return

        # At this point, the node to delete is the root
        node_to_delete = self.root
        
        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect left subtree from the node to be deleted
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to the root of the left subtree
            # Temporarily set the root to perform splay within the subtree
            self.root = left_subtree
            self._splay(max_node)

            # The new root (max_node) now has the right_subtree as its right child
            max_node.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_node
            
            self.root = max_node