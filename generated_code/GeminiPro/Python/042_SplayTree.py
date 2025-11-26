class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.

    This implementation includes insert, delete, and search operations. The search
    operation (and consequently insert and delete) performs a splay, moving the
    accessed node (or its parent/successor) to the root of the tree to optimize

    future accesses.
    """

    class _Node:
        """Internal class to represent a node in the Splay Tree."""
        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on node x."""
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
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
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        """
        Splays the node x to the root of the tree.
        This operation involves a sequence of rotations (Zig, Zig-Zig, Zig-Zag)
        to move the node up the tree.
        """
        while x.parent is not None:
            p = x.parent
            g = p.parent
            if g is None:  # Zig step
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
            elif x == p.right and p == g.left:  # Zig-Zag step
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag step (x == p.left and p == g.right)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last non-null node visited during the
        search is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node is not None:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key found, splay the node and return True
                self._splay(node)
                return True

        # Key not found, splay the last visited node (if any)
        if last_node is not None:
            self._splay(last_node)
        
        # After splaying, the root might be the key, but search failed before.
        # The return value should reflect the initial search result.
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted as a new node and then splayed to
        the root. This class implements a set, so duplicates are not stored.

        Args:
            key: The integer key to insert.
        """
        node = self.root
        parent = None
        while node is not None:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key already exists, splay it to the root
                self._splay(node)
                return

        # Insert the new key
        new_node = self._Node(key, parent)
        if parent is None:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The tree is first splayed on the key. If the key is found, it becomes
        the root. The root is then removed, and its left and right subtrees
        are joined together.

        Args:
            key: The integer key to delete.
        """
        # Splay the tree on the key. This brings the node (or its neighbor) to the root.
        # We perform the search-and-splay manually here to avoid an extra check.
        node = self.root
        last_node = None
        while node is not None:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                break # Found the node
        
        if last_node is not None:
            self._splay(last_node)
        
        # After splaying, if the root's key is not the target key, it wasn't in the tree.
        if self.root is None or self.root.key != key:
            return

        # The node to delete is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if left_subtree is None:
            self.root = right_subtree
            if self.root is not None:
                self.root.parent = None
        elif right_subtree is None:
            self.root = left_subtree
            if self.root is not None:
                self.root.parent = None
        else:
            # Disconnect both subtrees from the old root
            left_subtree.parent = None
            right_subtree.parent = None

            # Find the maximum element in the left subtree
            max_in_left = left_subtree
            while max_in_left.right is not None:
                max_in_left = max_in_left.right

            # Splay this maximum element to the root of the (now detached) left subtree.
            # We can temporarily set self.root to perform the splay in the correct context.
            self.root = left_subtree
            self._splay(max_in_left)

            # The new root is the max element from the left subtree.
            # Attach the original right subtree as its right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root