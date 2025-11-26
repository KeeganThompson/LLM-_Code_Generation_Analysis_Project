class SplayTree:
    """
    An implementation of a Splay Tree, a self-balancing binary search tree.
    This class provides a dictionary-like set for storing unique integer keys.
    """

    class _Node:
        """A node in the Splay Tree."""
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

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
        
        If the key is found, the corresponding node is splayed to the root and
        True is returned. If the key is not found, the last accessed node (the
        would-be parent) is splayed to the root and False is returned.

        Args:
            key (int): The key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        last_accessed = self.root
        current = self.root
        while current:
            last_accessed = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        if last_accessed:
            self._splay(last_accessed)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key does not exist, it is inserted and the new node is splayed
        to the root. If the key already exists, the existing node is splayed
        to the root.

        Args:
            key (int): The key to insert.
        """
        parent = None
        current = self.root
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:  # Key already exists
                self._splay(current)
                return

        # Key not found, insert new node
        new_node = self._Node(key)
        new_node.parent = parent

        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The tree is first searched for the key. The accessed node (or its
        parent if not found) is splayed. If the key was found at the root
        after splaying, it is removed.

        Args:
            key (int): The key to delete.
        """
        if not self.root:
            return

        # Search for the key and splay the accessed node
        self.search(key)

        # If the key is not at the root after splaying, it wasn't in the tree
        if self.root.key != key:
            return

        # Now, the node to delete is the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect left subtree to work on it
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Temporarily make the left subtree the main tree for splaying
            # This brings the max element to the root of the left subtree
            temp_root_backup = self.root
            self.root = left_subtree
            self._splay(max_in_left)
            
            # The new root is the max element from the left subtree.
            # Join the original right subtree to it.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root