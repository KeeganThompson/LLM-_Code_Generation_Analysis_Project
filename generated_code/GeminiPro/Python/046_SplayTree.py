import sys

class SplayTree:
    """
    A complete, self-contained SplayTree class that implements a
    dictionary-like set for integers.

    This implementation includes the essential methods: insert, delete, and search.
    The search operation (and by extension, insert and delete) performs a splay
    operation, moving the accessed node (or its parent if not found) to the root
    to optimize future accesses for that key.
    """

    class _Node:
        """A private node class for the SplayTree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation around the given node x."""
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
        """Performs a right rotation around the given node x."""
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
        This is the core operation of the Splay Tree, using zig, zig-zig,
        and zig-zag rotations.
        """
        while x.parent:
            p = x.parent
            g = p.parent  # Grandparent

            if not g:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay it and we're done
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        new_node = self._Node(key)
        new_node.parent = parent

        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last non-null node accessed during the
        search is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Key not found, splay the last visited node if it exists
        if last_node:
            self._splay(last_node)
            
        return False

    def delete(self, key):
        """
        Deletes a key from the tree.

        The operation first searches for the key, which splays the node (if found)
        or its would-be parent to the root. If the key is found, the node is
        removed, and its two subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. This splays the found node to the root.
        # If not found, it splays the would-be parent and returns False.
        if not self.search(key):
            return  # Key wasn't in the tree.

        # If search returned True, the node to delete is now the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # If a left subtree exists, we find its maximum element, splay it
            # to the root of the left subtree, and then attach the right subtree.
            left_subtree.parent = None
            
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay max_node to be the root of the left subtree.
            # We temporarily make the left subtree the main tree for the splay operation.
            self.root = left_subtree
            self._splay(max_node) # self.root is now max_node
            
            # Attach the original right subtree to the new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root