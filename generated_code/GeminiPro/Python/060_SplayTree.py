import sys

# To prevent recursion depth errors on large trees, though unlikely with splaying
# sys.setrecursionlimit(2000)

class SplayTree:
    """
    An implementation of a Splay Tree that acts as a dictionary-like set for integers.
    Splay trees are self-balancing binary search trees with the additional property
    that recently accessed elements are quick to access again.

    This implementation includes insert, delete, and search operations, with the
    characteristic splaying operation performed on each access.
    """

    class _Node:
        """A node in the splay tree."""
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
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
            else:  # Zig-Zag case
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        Performs the splaying operation on the accessed node if found,
        or on its parent if not found.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        node = self.root
        last_node = None
        while node:
            last_node = node
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        if last_node:
            self._splay(last_node)
        
        return self.root and self.root.key == key

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then the new node is splayed
        to the root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay the node and return
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Insert the new node
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
        Deletes a key from the tree.

        The standard splay tree deletion algorithm is used:
        1. Search for the key, which splays the node (or a nearby one) to the root.
        2. If the key is not at the root, it wasn't in the tree.
        3. If the key is at the root, remove it and join the two resulting subtrees.
           - To join, find the maximum element in the left subtree.
           - Splay this maximum element to the root of the left subtree.
           - Attach the right subtree as the right child of this new root.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Search splays the node or its parent to the root
        self.search(key)

        # If key is not at the root after splaying, it's not in the tree
        if self.root.key != key:
            return

        # Now the node to delete is at the root
        node_to_delete = self.root
        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if not left_subtree:
            # Promote the right subtree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # Promote the left subtree
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Join the two subtrees
            left_subtree.parent = None
            
            # Find the max element in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max element to the root of the left subtree
            # by temporarily treating the left subtree as the main tree.
            self.root = left_subtree
            self._splay(max_node)
            
            # Now self.root is the max_node. Attach the original right subtree.
            self.root.right = right_subtree
            right_subtree.parent = self.root