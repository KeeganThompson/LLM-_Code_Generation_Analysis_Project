class SplayTree:
    """
    An implementation of a Splay Tree.
    
    This class provides a dictionary-like set for integers with methods for
    insertion, deletion, and searching. The key feature is the splaying
    operation, which moves an accessed node to the root of the tree to
    optimize future accesses based on the principle of locality.
    """

    class _Node:
        """A node in the splay tree."""
        __slots__ = 'key', 'parent', 'left', 'right'

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

    def _splay(self, p):
        """
        Performs the splay operation on node p, moving it to the root.
        """
        if not p:
            return
        while p.parent:
            parent = p.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case: Parent is the root
                if p == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif p == parent.left and parent == grandparent.left:
                # Zig-zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif p == parent.right and parent == grandparent.right:
                # Zig-zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif p == parent.right and parent == grandparent.left:
                # Zig-zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:
                # Zig-zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the would-be parent)
        is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_node = self.root
        while current:
            last_node = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node
        self._splay(last_node)
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
            if key == current.key:
                # Key already exists, splay it and return
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        The node containing the key is first splayed to the root, then removed.
        If the key is not found, the tree structure is modified by the splay
        operation from the search, but no key is removed.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. If found, it will be splayed to the root.
        if not self.search(key):
            # Key not in tree, nothing to do.
            # search() has already splayed the last visited node.
            return

        # At this point, the node to delete is the root
        z = self.root
        
        # Case 1: No left child
        if not z.left:
            self.root = z.right
            if self.root:
                self.root.parent = None
        # Case 2: No right child
        elif not z.right:
            self.root = z.left
            if self.root:
                self.root.parent = None
        # Case 3: Both children exist
        else:
            # Isolate the left and right subtrees
            left_subtree = z.left
            right_subtree = z.right
            left_subtree.parent = None
            right_subtree.parent = None

            # Find the maximum node in the left subtree
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Splay this maximum node to the root of the left subtree.
            # We temporarily make the left subtree the main tree to do this.
            self.root = left_subtree
            self._splay(max_in_left)
            
            # Now, the new root (max_in_left) has no right child.
            # We can attach the original right subtree to it.
            self.root.right = right_subtree
            right_subtree.parent = self.root