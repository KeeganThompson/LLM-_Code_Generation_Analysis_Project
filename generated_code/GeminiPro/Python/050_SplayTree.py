class SplayTree:
    """
    An implementation of a Splay Tree, a self-balancing binary search tree.
    This class provides a dictionary-like set for storing unique integers.
    The main operations (insert, delete, search) trigger a 'splaying'
    operation, which moves the accessed element (or its closest neighbor)
    to the root of the tree, optimizing for future accesses.
    """

    class _Node:
        """A node in the splay tree, intended for internal use."""
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

    def _splay(self, node):
        """
        Performs the splaying operation on a node, moving it to the root.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig step
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
        Performs the splaying operation on the accessed node if found,
        or on its parent if not found, moving it to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = self.root
        while current:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found, splay the node and return True
                self._splay(current)
                return True
        
        # Key not found, splay the last visited node and return False
        self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree. If the key already exists, the tree
        is splayed on that key, but no duplicate is inserted.

        Args:
            key: The integer key to insert.
        """
        # Case 1: The tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree on the key. This brings the closest node to the root.
        # We traverse to find the insertion point or existing node.
        current = self.root
        parent = None
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and we are done.
                self._splay(current)
                return
        
        # Key was not found, splay the last visited node (the parent).
        self._splay(parent)

        # Now, the splayed parent is at the root. We insert the new key
        # and restructure the tree by splitting.
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
            if new_node.left:
                new_node.left.parent = new_node
            self.root.parent = new_node
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
            if new_node.right:
                new_node.right.parent = new_node
            self.root.parent = new_node
        
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree. If the key is not found, the tree
        is splayed on the last accessed node, but no deletion occurs.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay on the key. This brings the node (or its would-be parent) to the root.
        self.search(key)

        # After search, if root's key isn't the one we're looking for, it wasn't in the tree.
        if self.root.key != key:
            return
        
        # The node to delete is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # Promote the left subtree.
            self.root = left_subtree
            self.root.parent = None
        else:
            # Both subtrees exist. Join them.
            # 1. Disconnect left subtree.
            left_subtree.parent = None

            # 2. Find the max element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # 3. Splay this max element to be the root of the left subtree.
            #    Temporarily set the tree's root to the left subtree's root.
            self.root = left_subtree
            self._splay(max_node) # After this, self.root is max_node

            # 4. The new root of the whole tree is this splayed max_node.
            #    Attach the original right subtree to it.
            self.root.right = right_subtree
            right_subtree.parent = self.root