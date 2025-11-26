class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.

    This class provides a dictionary-like set for integers, supporting
    insert, delete, and search operations. The key feature of a splay tree
    is that recently accessed elements are moved to the root of the tree
    to optimize for temporal locality, providing good amortized performance.
    """

    class _Node:
        """A node in the Splay Tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

        def __repr__(self):
            return f"_Node({self.key})"

    def __init__(self):
        """Initializes an empty Splay Tree."""
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        y.right = x
        x.parent = y

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.
        """
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
        Searches for a key in the tree.

        Performs the splaying operation on the accessed node if found,
        or on its parent if the node is not found.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_visited = None
        while node:
            last_visited = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key found, splay the node and return
                self._splay(node)
                return True
        
        # Key not found, splay the last visited node (parent)
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        Otherwise, the new key is inserted and becomes the new root.

        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree on the key. This brings the closest key to the root.
        self.search(key)

        # If the key is already present, search would have splayed it and we are done.
        if self.root.key == key:
            return

        # Otherwise, insert the new node and make it the root
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if new_node.left:
                new_node.left.parent = new_node
            self.root.parent = new_node
            self.root.left = None
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if new_node.right:
                new_node.right.parent = new_node
            self.root.parent = new_node
            self.root.right = None
        
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is found, it is deleted. The tree is re-structured
        by splaying the maximum element of the left subtree to its root
        and then joining it with the right subtree.

        Args:
            key: The integer key to delete.
        """
        # Splay the tree on the key. If not found, splay brings the closest
        # node to the root and we can return.
        if not self.search(key):
            return

        # After search, if the key was found, it is at the root.
        left_tree = self.root.left
        right_tree = self.root.right

        if not left_tree:
            # Promote the right subtree to be the new root
            self.root = right_tree
            if right_tree:
                right_tree.parent = None
        else:
            # Detach the left subtree
            left_tree.parent = None
            
            # Find the maximum element in the left subtree
            max_node = left_tree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to the root of the left subtree.
            # We can do this by temporarily setting the root to the left subtree's
            # root and then performing the splay operation.
            self.root = left_tree
            self._splay(max_node)

            # After splaying, max_node is the new root of the combined left part.
            # Attach the original right subtree to the new root.
            self.root.right = right_tree
            if right_tree:
                right_tree.parent = self.root

    def __contains__(self, key):
        """Allows for 'in' operator syntax (e.g., 'if key in tree:')."""
        return self.search(key)

    def __str__(self):
        """Returns an in-order string representation of the tree."""
        if not self.root:
            return "SplayTree()"
        keys = []
        def _inorder_traversal(node):
            if node:
                _inorder_traversal(node.left)
                keys.append(str(node.key))
                _inorder_traversal(node.right)
        
        _inorder_traversal(self.root)
        return f"SplayTree({', '.join(keys)})"

    def __repr__(self):
        return self.__str__()