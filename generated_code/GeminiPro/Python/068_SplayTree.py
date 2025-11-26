class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class provides a dictionary-like set for storing unique integer keys.
    It supports insertion, deletion, and searching. The key feature is the
    splaying operation: whenever a key is accessed (searched, inserted, or
    deleted), the corresponding node is moved to the root of the tree to
    optimize for future accesses.
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
        This is done by a series of rotations (Zig, Zig-Zig, Zig-Zag)
        until the node x is the root of the tree.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
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
        Searches for a key in the tree and performs the splaying operation.
        
        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last non-null node visited during the search
        (the would-be parent) is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_visited = None
        while node:
            last_visited = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # If key is not found, splay the last visited node.
        if last_visited:
            self._splay(last_visited)
        
        return False

    def insert(self, key):
        """
        Inserts a key into the splay tree.

        If the key already exists, the node is splayed to the root.
        If the key is new, it is inserted as in a standard BST and then
        the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay it and return.
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Insert the new node.
        new_node = self._Node(key)
        new_node.parent = parent
        
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
            
        # Splay the newly inserted node to the root.
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the splay tree.

        The tree is first searched for the key, which brings the node (or its
        closest neighbor) to the root. If the key is present, the node (now at the
        root) is removed, and its two subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. This splays the node to the root if found.
        if not self.search(key):
            # Key not in the tree. search() has already splayed the closest node.
            return
        
        # After a successful search, the node to delete is at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Find the maximum element in the left subtree.
            # This element will become the new root.
            left_subtree.parent = None  # Disconnect from old root
            
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node. It becomes the new root of the combined tree.
            # We temporarily set the tree's root to the left_subtree to perform
            # the splay within that context.
            self.root = left_subtree
            self._splay(max_node)
            
            # Now self.root is max_node. Re-attach the original right subtree.
            # After splaying the max node, its right child is guaranteed to be None.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root