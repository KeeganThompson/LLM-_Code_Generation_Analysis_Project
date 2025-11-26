class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.

    This data structure acts as a dictionary-like set for storing unique integers.
    It supports `insert`, `delete`, and `search` operations. The defining
    feature of a Splay Tree is its self-balancing mechanism: whenever a key
    is accessed, it is moved to the root of the tree through a series of
    rotations. This "splaying" operation makes frequently accessed elements
    faster to retrieve over time.
    """

    class _Node:
        """A private node class for the Splay Tree."""
        __slots__ = 'key', 'parent', 'left', 'right'

        def __init__(self, key: int, parent: 'SplayTree._Node' = None,
                     left: 'SplayTree._Node' = None, right: 'SplayTree._Node' = None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root: SplayTree._Node | None = None

    def _rotate_left(self, x: _Node):
        """Performs a left rotation on the given node x."""
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

    def _rotate_right(self, x: _Node):
        """Performs a right rotation on the given node x."""
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

    def _splay(self, node: _Node):
        """
        Performs the splaying operation on a node, moving it to the root.
        """
        if not node:
            return
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
                if node == parent.left:
                    self._rotate_right(parent)
                else:
                    self._rotate_left(parent)
            elif node == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._rotate_right(grandparent)
                self._rotate_right(parent)
            elif node == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._rotate_left(grandparent)
                self._rotate_left(parent)
            elif node == parent.right and parent == grandparent.left:
                # Zig-Zag case (left-right)
                self._rotate_left(parent)
                self._rotate_right(grandparent)
            else:
                # Zig-Zag case (right-left)
                self._rotate_right(parent)
                self._rotate_left(grandparent)
        self.root = node

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the
        root and the method returns True.
        If the key is not found, the last node visited before the search
        terminated is splayed to the root, and the method returns False.

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
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found
                self._splay(current)
                return True

        # Key not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key: int):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.

        Args:
            key: The integer key to insert.
        """
        # Case 1: The tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree on the key. The root will be the closest node.
        # This conveniently brings the relevant part of the tree to the top.
        self.search(key)

        # After splaying, check if the key is already at the root.
        if self.root.key == key:
            return  # Key already exists

        # Case 2: Insert the new node and restructure the tree
        new_node = self._Node(key)
        if key < self.root.key:
            # New node becomes the root.
            # Old root becomes the right child of the new node.
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
            self.root.parent = new_node
        else:  # key > self.root.key
            # New node becomes the root.
            # Old root becomes the left child of the new node.
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None
            self.root.parent = new_node

        self.root = new_node

    def delete(self, key: int):
        """
        Deletes a key from the tree.

        The tree is first splayed on the key. If the key exists, it is
        removed, and its two subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        # Splay the node to be deleted (or its parent) to the root.
        if not self.search(key):
            # Key was not found, so nothing to delete.
            # The search call already splayed the closest node.
            return

        # At this point, the node with the key is guaranteed to be the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left child, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree to work on it.
            left_subtree.parent = None

            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum node to the root of the (temporary) left subtree.
            # We can do this by temporarily setting self.root.
            self.root = left_subtree
            self._splay(max_node)

            # After splaying, self.root is the max_node. It has no right child.
            # We can now attach the original right subtree to it.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root