class SplayTree:
    """
    A complete, self-contained Python class that implements a dictionary-like
    set for integers using a Splay Tree.

    This data structure provides amortized O(log n) time complexity for insert,
    delete, and search operations. The key feature of a splay tree is that
    recently accessed elements are moved to the root of the tree, which can
    improve performance for certain access patterns (e.g., temporal locality).
    """

    # Nested class for tree nodes
    class _Node:
        """A node in the splay tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
        self.root = None

    # --- Private Helper Methods ---

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

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.
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
            elif x == parent.right and parent == grandparent.left:  # Zig-Zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (x is left child of right child)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    # --- Public API Methods ---

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, the node with that key is splayed to the root.
        If the key does not exist, a new node is created, inserted, and then
        splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
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

        # Key does not exist, create and insert new node
        new_node = self._Node(key)
        new_node.parent = parent

        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node to the root
        self._splay(new_node)

    def search(self, key):
        """
        Searches for a key in the tree.

        This method performs the splaying operation. If the key is found, the
        node containing the key is moved to the root. If the key is not found,
        the last non-null node accessed during the search is moved to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
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
                # Key found, splay the node
                self._splay(node)
                return True
        
        # Key not found, splay the last accessed node (parent of where key would be)
        if last_node:
            self._splay(last_node)
        return False

    def delete(self, key):
        """
        Deletes a key from the tree.

        The search for the key involves a splay operation. If the key is found,
        it is removed, and its subtrees are merged. The in-order predecessor
        (the maximum element in the left subtree) becomes the new root. If the
        key is not found, the tree is splayed based on the last accessed node
        but no deletion occurs.

        Args:
            key (int): The integer key to delete.
        """
        # Search for the key, which splays the node (or its parent) to the root
        if not self.search(key):
            # Key was not found, search() already splayed the tree appropriately
            return

        # After search(key), if the key was found, it's now at the root.
        # However, search() returns true only if root.key == key.
        # We double-check to be safe, especially for an empty tree.
        if self.root is None or self.root.key != key:
            return
        
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        elif not right_subtree:
            # No right child, so the left subtree becomes the new tree
            self.root = left_subtree
            if left_subtree:
                left_subtree.parent = None
        else:
            # Both children exist. We need to merge the two subtrees.
            # 1. Make the left subtree the main tree for a moment.
            # 2. Find the maximum element in the left subtree.
            # 3. Splay this maximum element to the root of the left subtree.
            # 4. Attach the right subtree as the right child of the new root.
            
            # Disconnect left subtree from the old root
            left_subtree.parent = None
            
            # Find the max node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Temporarily set the root to perform the splay on the subtree
            self.root = left_subtree
            self._splay(max_node)
            
            # Now, self.root is the max_node of the old left subtree.
            # It has no right child. We can attach the original right subtree.
            self.root.right = right_subtree
            right_subtree.parent = self.root