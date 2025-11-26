class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class provides a dictionary-like set for storing unique integer keys.
    A splay tree is a self-adjusting binary search tree with the property
    that recently accessed elements are quick to access again. It achieves this
    by moving any accessed node to the root of the tree through a series of
    rotations, a process called "splaying".

    The amortized time complexity for search, insert, and delete operations
    is O(log n), where n is the number of nodes in the tree.
    """

    class _Node:
        """A private inner class representing a node in the Splay Tree."""
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

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.

        The splaying is done through a series of rotations (Zig, Zig-Zig,
        or Zig-Zag) until the node x becomes the root of the tree.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig step
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig step
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig step
                self._left_rotate(g)
                self._left_rotate(p)
            else:  # Zig-Zag step
                if x == p.right and p == g.left:
                    self._left_rotate(p)
                    self._right_rotate(g)
                else:  # x == p.left and p == g.right
                    self._right_rotate(p)
                    self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree and performs the splaying operation.

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last node accessed during the search
        (the would-be parent) is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = None
        while current:
            last_visited = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
            
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

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
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and return
                self._splay(current)
                return
        
        # Insert the new node as in a standard BST
        new_node = self._Node(key, parent=parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        This method first searches for the key, which splays the relevant node
        to the root. If the key is found, the node (now at the root) is removed
        and the remaining subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        # Search splays the node to the root if found, or the parent if not.
        if not self.search(key):
            # Key was not in the tree. search() has already splayed the last
            # accessed node, so we can just return.
            return

        # If search returned True, the node to delete is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree from the old root.
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree. This will be the
            # new root of the combined tree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to the root of the left subtree.
            # We temporarily set self.root to the left subtree's root to
            # confine the splay operation within that subtree.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, max_node is the new root of the left part.
            # It has no right child. We can now attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root