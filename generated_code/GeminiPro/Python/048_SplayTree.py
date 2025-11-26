class SplayTree:
    """
    An implementation of a Splay Tree that acts as a dictionary-like set for integers.
    Splay trees are self-balancing binary search trees with the additional property
    that recently accessed elements are quick to access again.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
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
            else:  # Zig-Zag case (x is left child, parent is right child)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        Performs the splaying operation on the accessed node or its would-be parent.
        Returns True if the key is found, False otherwise.
        """
        node = self.root
        last_visited = None
        found = False

        while node:
            last_visited = node
            if key == node.key:
                found = True
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        if node:  # Key was found
            self._splay(node)
        elif last_visited:  # Key not found, splay the last visited node
            self._splay(last_visited)

        return found

    def insert(self, key):
        """
        Inserts a key into the tree.
        If the key already exists, the tree remains unchanged but the existing
        node with the key is splayed to the root.
        """
        # If tree is empty, create a new root
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the closest node to the root
        self.search(key)

        # If key is already at the root, we're done
        if self.root.key == key:
            return

        # Otherwise, split the tree and insert the new node as the root
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.parent = new_node
            self.root.left = None
        else: # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.parent = new_node
            self.root.right = None
        
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.
        If the key is not found, the tree structure may change due to splaying,
        but no node is removed.
        """
        # Splay the node to be deleted (or its parent) to the root
        self.search(key)

        # If the key is not at the root, it wasn't in the tree
        if not self.root or self.root.key != key:
            return

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If no left subtree, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Detach the left subtree
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this max node to the root of the left subtree
            # Temporarily set root to perform splay within the subtree
            self.root = left_subtree
            self._splay(max_node)

            # The new root (max_node) now has the right_subtree as its right child
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root