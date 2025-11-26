class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class provides a dictionary-like set for integers, supporting
    insert, delete, and search operations. The key feature of a splay tree
    is that recently accessed elements are moved to the root of the tree
    to optimize for temporal locality of reference.
    """

    class _Node:
        """A private helper class representing a node in the splay tree."""
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
        Splays the given node to the root of the tree through a series of rotations.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:
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
        if not self.root:
            return False

        current = self.root
        last_visited = self.root
        while current:
            last_visited = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node (the parent)
        self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the splay tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and we're done
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Insert the new node as in a standard BST
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the splay tree.

        The search for the key will cause a splay. If the key is found, it is
        splayed to the root and then deleted. The resulting two subtrees are
        joined. After deletion, the parent of the (now-deleted) node becomes
        the root of its subtree. If the key is not found, the last accessed
        node during the search is splayed to the root.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # This search will splay the node if found, or its parent if not found.
        if not self.search(key):
            # Key was not in the tree; search() already splayed the would-be parent.
            return

        # At this point, the node to delete is the root due to search()
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Find the maximum node in the left subtree.
            # This node will become the new root of the combined tree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Temporarily make the left subtree the main tree to splay within it.
            self.root = left_subtree
            left_subtree.parent = None
            
            # Splay the max_node to the root of this subtree.
            # After this, max_node has no right child.
            self._splay(max_node)
            
            # Attach the original right subtree to the new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root