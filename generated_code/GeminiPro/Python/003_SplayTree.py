class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.

    This implementation includes insert, delete, and search operations.
    The key feature of a splay tree is that recently accessed elements are moved
    to the root of the tree to optimize for temporal locality, making subsequent
    accesses to the same element faster.
    """

    class _Node:
        """A private nested class to represent a node in the Splay Tree."""
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
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig case
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig case
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last accessed node (the parent of the
        null link where the search terminated) is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        last_visited = None
        current = self.root
        while current:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                self._splay(current)
                return True

        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        Otherwise, a new node is created and inserted, then becomes the new root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Search splays the closest node to the root
        self.search(key)

        # If key is already present, search would have splayed it to the root
        if self.root.key == key:
            return

        new_node = self._Node(key)
        old_root = self.root

        if key < old_root.key:
            new_node.right = old_root
            new_node.left = old_root.left
            if old_root.left:
                old_root.left.parent = new_node
            old_root.left = None
        else: # key > old_root.key
            new_node.left = old_root
            new_node.right = old_root.right
            if old_root.right:
                old_root.right.parent = new_node
            old_root.right = None

        old_root.parent = new_node
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key exists, it's splayed to the root and then removed. The tree
        is then re-joined. If the key does not exist, the last accessed node
        is splayed, and the tree remains unchanged.

        Args:
            key: The integer key to delete.
        """
        # Splay the node to the root. If not found, splay the parent.
        if not self.search(key):
            # Key not in tree, nothing to delete.
            # search() already splayed the last accessed node.
            return

        # After search, if the key was found, it is now the root.
        # This check is technically redundant if search() returns True, but safe.
        if self.root.key != key:
            return

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect left subtree
            left_subtree.parent = None

            # Find the maximum element in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum element to be the root of the left subtree
            # Temporarily set self.root to perform splay within the subtree
            temp_root = self.root
            self.root = left_subtree
            self._splay(max_node)
            # self.root is now max_node, which is the new root of the whole tree

            # Attach the original right subtree
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root