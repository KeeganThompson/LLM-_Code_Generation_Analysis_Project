class SplayTree:
    """
    A self-contained Python class that implements a Splay Tree.
    This tree acts as a dictionary-like set for storing unique integer keys.
    
    The core feature is the splay operation: whenever a key is accessed 
    (for searching, insertion, or deletion), the corresponding node is moved 
    to the root of the tree, making subsequent accesses to that key faster.
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
        Performs the splay operation on a node, moving it to the root.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            
            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        This method performs the splaying operation on the accessed node. If the
        key is found, its node is moved to the root. If the key is not found,
        the last accessed node (the parent where the key would have been) is
        splayed to the root.
        
        Args:
            key: The integer key to search for.
        
        Returns:
            True if the key is found, False otherwise.
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
        
        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted as a new node and then that new node
        is splayed to the root.
        
        Args:
            key: The integer key to insert.
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
        
        This operation first searches for the key, which brings the node
        (or its potential parent) to the root. If the key is found, the node
        is removed and the tree is re-joined.
        
        Args:
            key: The integer key to delete.
        """
        # Splay the node with the given key (or its would-be parent) to the root.
        if not self.search(key):
            # Key is not in the tree. search() already splayed the last visited node.
            return

        # At this point, the node to be deleted is the root.
        z = self.root
        
        left_subtree = z.left
        right_subtree = z.right

        if not left_subtree:
            # Promote the right subtree to be the new root.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        elif not right_subtree:
            # Promote the left subtree to be the new root.
            self.root = left_subtree
            if left_subtree:
                left_subtree.parent = None
        else:
            # Both subtrees exist. Join them.
            # Disconnect left subtree from the old root.
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this max_node. We temporarily set self.root to perform
            # the splay within the left subtree.
            self.root = left_subtree
            self._splay(max_node)

            # The new root is max_node. Attach the original right subtree.
            # After splaying, max_node is guaranteed to have no right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root