class SplayTree:
    """
    A self-contained Python class implementing a dictionary-like set for integers
    using a Splay Tree.

    This data structure provides amortized O(log n) time complexity for search,
    insert, and delete operations. The key feature is the splaying operation,
    which moves frequently accessed elements closer to the root of the tree,
    optimizing subsequent lookups for those elements.
    """

    class _Node:
        """A private helper class representing a node in the Splay Tree."""
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
            y.left = x
            x.parent = y

    def _right_rotate(self, x):
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
            y.right = x
            x.parent = y

    def _splay(self, node):
        """
        Splays the given node to the root of the tree using a series of
        zig, zig-zig, and zig-zag rotations.
        """
        if not node:
            return

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
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last node visited before the search failed
        (the would-be parent) is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
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

        # If key is not found, splay the last visited node (if any).
        if last_visited:
            self._splay(last_visited)

        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted as in a standard BST and then the
        new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        parent = None
        current = self.root
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and we are done.
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        # Insert the new node as a child of the parent.
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root.
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        First, the tree is splayed on the key. If the key exists, it becomes
        the root. The tree is then split into two subtrees (left and right),
        and the largest element of the left subtree is splayed to its root
        and then joined with the right subtree.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. This splays the node to the root if found,
        # or its would-be parent if not found.
        if not self.search(key):
            # Key is not in the tree, nothing to delete.
            return

        # At this point, the node to delete is the root because search() splayed it.
        node_to_delete = self.root
        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree from the old root.
            left_subtree.parent = None

            # Find the maximum element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this max element to the root of the (now separated) left subtree.
            self.root = left_subtree
            self._splay(max_node)

            # The new root (the former max_node) has no right child.
            # Attach the original right subtree as its right child.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root