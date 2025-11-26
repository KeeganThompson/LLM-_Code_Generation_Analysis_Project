class SplayTree:
    """
    Implements a splay tree that functions as a dictionary-like set for integers.

    A splay tree is a self-adjusting binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up and removal in
    O(log n) amortized time.
    """

    class _Node:
        """A node in the splay tree."""
        __slots__ = 'key', 'parent', 'left', 'right'

        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
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
        if y:
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
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.
        """
        if not x:
            return
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig case (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig case (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag case (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag case (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for an integer key in the tree.
        Performs the splaying operation on the accessed node (if found) or its
        parent (if not found) to move it to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        last_node = None
        node = self.root
        while node:
            last_node = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Key not found, splay the last visited node (the would-be parent)
        if last_node:
            self._splay(last_node)

        return False

    def insert(self, key):
        """
        Inserts an integer key into the tree.
        If the key already exists, the corresponding node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        # Case 1: The tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree around the key. If the key exists, it becomes the root.
        # If not, the node that would be its parent becomes the root.
        self.search(key)

        # If the key is already at the root, we're done.
        if self.root.key == key:
            return

        # Insert the new key and make it the new root
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.left = self.root.left
            if new_node.left:
                new_node.left.parent = new_node

            new_node.right = self.root
            self.root.parent = new_node
            self.root.left = None
        else:  # key > self.root.key
            new_node.right = self.root.right
            if new_node.right:
                new_node.right.parent = new_node

            new_node.left = self.root
            self.root.parent = new_node
            self.root.right = None

        self.root = new_node

    def delete(self, key):
        """
        Deletes an integer key from the tree.
        The tree is first splayed on the key. If the key is found, its node
        is removed. The remaining subtrees are joined, and the new root is
        the result of a splay operation within one of the subtrees. If the
        key is not found, the last accessed node is splayed to the root.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the node to the root. If not found, splay its would-be parent.
        if not self.search(key):
            # Key not found, nothing to delete. search() already splayed.
            return

        # At this point, the node to delete is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if left_subtree:
            left_subtree.parent = None
        if right_subtree:
            right_subtree.parent = None

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the tree.
            self.root = right_subtree
        else:
            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this maximum node to the root of the left subtree.
            # After this, it will have no right child.
            # Temporarily set the root to the left subtree for the splay call.
            temp_root = self.root
            self.root = left_subtree
            self._splay(max_node)
            # self.root is now max_node

            # Join the original right subtree to the new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root