class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.
    
    This implementation includes insert, delete, and search operations, all of which
    involve the characteristic splaying step to move the accessed node (or its
    parent/successor) to the root of the tree. This optimizes future accesses
    to recently used keys.
    """

    class _Node:
        """A private inner class to represent a node in the Splay Tree."""
        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on the subtree rooted at node x."""
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
        """Performs a right rotation on the subtree rooted at node x."""
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
        Performs the splaying operation on a node, moving it to the root.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def insert(self, key):
        """
        Inserts a key into the Splay Tree.
        
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then the new node is splayed to the root.
        
        Args:
            key (int): The integer key to insert.
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
            else:  # Key already exists
                self._splay(node)
                return
        
        # Key does not exist, insert new node
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def search(self, key):
        """
        Searches for a key in the Splay Tree.
        
        If the key is found, the corresponding node is splayed to the root and True is returned.
        If the key is not found, the last accessed node (the would-be parent) is splayed
        to the root and False is returned.
        
        Args:
            key (int): The integer key to search for.
            
        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        node = self.root
        last_visited = self.root
        while node:
            last_visited = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:  # Key found
                self._splay(node)
                return True
        
        # Key not found, splay the last visited node
        self._splay(last_visited)
        return False

    def delete(self, key):
        """
        Deletes a key from the Splay Tree.
        
        The tree is first searched for the key, which brings the node (or its parent)
        to the root. If the key is found at the root, it is removed and the remaining
        subtrees are joined.
        
        Args:
            key (int): The integer key to delete.
        """
        if not self.root:
            return

        # Search for the key, which splays the node (or its parent) to the root
        self.search(key)

        # After search, if the root's key is not the one we want to delete,
        # the key was not in the tree.
        if self.root.key != key:
            return

        # Now, the node to delete is at the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left subtree, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Detach the left subtree
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Splay this maximum element to the root of the left subtree.
            # We can temporarily treat the left subtree as the main tree
            # to reuse the _splay method.
            self.root = left_subtree
            self._splay(max_in_left)
            
            # The new root of the combined tree is the splayed max_node.
            # Attach the original right subtree to its right.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root