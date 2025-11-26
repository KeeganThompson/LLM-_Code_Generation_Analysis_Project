class SplayTree:
    """
    A complete, self-contained implementation of a dictionary-like set for integers
    using a Splay Tree.

    A splay tree is a self-adjusting binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up, and removal
    in O(log n) amortized time.

    This class provides the following methods:
    - insert(key): Adds an integer key to the set.
    - delete(key): Removes an integer key from the set.
    - search(key): Checks if a key exists and splays the accessed node.
    """

    class _Node:
        """A private node class for the Splay Tree."""
        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty SplayTree."""
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

            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-zig (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-zig (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-zag (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-zag (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        This method performs the splaying operation on the accessed node to move
        it to the root. If the key is not found, the last accessed node (the
        would-be parent) is splayed to the root instead.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = None
        found = False

        while current:
            last_visited = current
            if key == current.key:
                found = True
                break
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        if last_visited:
            self._splay(last_visited)

        return found

    def insert(self, key):
        """
        Inserts a key into the tree. If the key already exists, the tree
        is splayed but not modified.

        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree around the key. This brings the closest node to the root.
        self.search(key)

        # After splaying, if the key is already in the tree, it's at the root.
        if self.root.key == key:
            return  # Key already exists

        # Key does not exist, so insert the new node at the root and restructure.
        new_node = self._Node(key)

        if key < self.root.key:
            # New node becomes root; old root becomes its right child.
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
        else:  # key > self.root.key
            # New node becomes root; old root becomes its left child.
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None

        self.root.parent = new_node
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree. If the key is not found, the tree is
        splayed around the closest key but is otherwise not modified.

        Args:
            key (int): The integer key to delete.
        """
        # Splay the tree. If the key exists, it becomes the new root.
        if not self.search(key) or self.root.key != key:
            # Key was not found, so nothing to delete. search() already splayed.
            return

        # At this point, the node to delete is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree to be the new root.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # Promote the left subtree to be the new root.
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. We need to join them.
            # 1. Detach the left subtree.
            left_subtree.parent = None

            # 2. Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # 3. Splay this max_node to the root of the (temporary) left subtree.
            #    We achieve this by temporarily setting the root for the splay operation.
            self.root = left_subtree
            self._splay(max_node)  # After this, self.root is max_node.

            # 4. Attach the original right subtree as the right child of the new root.
            #    The new root (max_node) is guaranteed to have no right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root