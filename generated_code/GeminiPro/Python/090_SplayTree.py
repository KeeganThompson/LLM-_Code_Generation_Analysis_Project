class SplayTree:
    """
    A complete, self-contained Python class that implements a splay tree.

    This class provides a dictionary-like set for integers, supporting
    insert, delete, and search operations. The key feature is the splaying
    operation, which moves an accessed node to the root to optimize
    future accesses, providing good amortized performance.
    """

    class _Node:
        """A private class representing a node in the splay tree."""
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
        Performs the splay operation on node x, moving it to the root.
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
            else:  # Zig-Zag step
                if x == p.right and p == g.left:
                    self._left_rotate(p)
                    self._right_rotate(g)
                else: # x == p.left and p == g.right
                    self._right_rotate(p)
                    self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree and performs the splaying operation.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the parent of where
        the key would be) is splayed to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = None
        while current is not None:
            last_visited = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last non-null node visited
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed
        to the root.

        Args:
            key (int): The integer key to insert.
        """
        # Phase 1: Search for the key's position like in a standard BST
        node = self.root
        parent = None
        while node is not None:
            parent = node
            if key == node.key:
                # Key already exists, splay it and we are done.
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        # Phase 2: Insert the new node
        new_node = self._Node(key, parent)
        if parent is None:  # The tree was empty
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Phase 3: Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The deletion process first splays the node with the given key to the
        root. If it exists, it is removed, and the remaining two subtrees
        are joined.

        Args:
            key (int): The integer key to delete.
        """
        # Splay the node with the key (or its would-be parent) to the root
        if not self.search(key):
            # Key not found. search() already splayed the closest node.
            return

        # At this point, the node to delete is the root, because search(key)
        # found it and splayed it.
        node_to_delete = self.root
        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if left_subtree is None:
            # Promote the right subtree to be the new root
            self.root = right_subtree
            if right_subtree is not None:
                right_subtree.parent = None
        else:
            # 1. Detach the left subtree
            left_subtree.parent = None
            
            # 2. Find the maximum element in the left subtree
            max_in_left = left_subtree
            while max_in_left.right is not None:
                max_in_left = max_in_left.right
            
            # 3. Splay this maximum element. It becomes the new root of the
            #    (temporarily separated) left subtree.
            self.root = left_subtree # Temporarily treat left subtree as the whole tree
            self._splay(max_in_left)
            
            # 4. The new root (max_in_left) now has no right child.
            #    Attach the original right subtree there.
            self.root.right = right_subtree
            if right_subtree is not None:
                right_subtree.parent = self.root