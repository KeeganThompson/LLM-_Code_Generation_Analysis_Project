class SplayTree:
    """
    A self-contained Python class implementing a dictionary-like set for integers
    using a Splay Tree.

    A splay tree is a self-balancing binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up and removal
    in O(log n) amortized time.
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

    def _rotate_left(self, x):
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

    def _rotate_right(self, x):
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
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            elif x == p.left and p == g.left:  # Zig-Zig case (left-left)
                self._rotate_right(g)
                self._rotate_right(p)
            elif x == p.right and p == g.right:  # Zig-Zig case (right-right)
                self._rotate_left(g)
                self._rotate_left(p)
            elif x == p.right and p == g.left:  # Zig-Zag case (left-right)
                self._rotate_left(p)
                self._rotate_right(g)
            else:  # Zig-Zag case (right-left)
                self._rotate_right(p)
                self._rotate_left(g)

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
        if not self.root:
            return False

        node = self.root
        parent = None
        while node is not None and node.key != key:
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        target_to_splay = None
        if node is not None:
            # Key found, splay the node itself
            target_to_splay = node
        elif parent is not None:
            # Key not found, splay the last accessed node
            target_to_splay = parent

        if target_to_splay:
            self._splay(target_to_splay)
        
        return self.root and self.root.key == key

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree for the key. This brings the closest node to the root.
        self.search(key)

        # If key is already at the root, we're done.
        if self.root.key == key:
            return

        # Otherwise, insert the new key and restructure the tree.
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.parent = new_node
            self.root.left = None
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.parent = new_node
            self.root.right = None
        
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is found, it is removed, and its parent (in the modified tree)
        is splayed. If the key is not found, the last accessed node is splayed.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node to be deleted (or its would-be parent) to the root.
        self.search(key)

        # If the key is not at the root, it wasn't in the tree.
        if not self.root or self.root.key != key:
            return

        # The node to delete is now the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Left subtree exists.
            # Disconnect it from the old root.
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max node to the root of the (now separated) left subtree.
            # We can do this by temporarily setting self.root and using _splay.
            temp_root_backup = self.root
            self.root = left_subtree
            self._splay(max_node) # After this, max_node is self.root
            
            # The new root of the whole tree is the splayed max_node.
            # Attach the original right subtree to it.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root