class SplayTree:
    """
    An implementation of a dictionary-like set for integers using a Splay Tree.
    
    This class provides insert, delete, and search operations. The key feature
    is the splaying operation, which moves frequently accessed elements to the
    root of the tree to optimize future lookups.
    """

    class _Node:
        """A private node class for the Splay Tree."""
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
        Performs the splaying operation on a node, moving it to the root.
        """
        while node.parent:
            # Zig case: Node is a direct child of the root
            if not node.parent.parent:
                if node == node.parent.left:
                    self._right_rotate(node.parent)
                else:
                    self._left_rotate(node.parent)
            # Zig-Zig case
            elif node == node.parent.left and node.parent == node.parent.parent.left:
                self._right_rotate(node.parent.parent)
                self._right_rotate(node.parent)
            elif node == node.parent.right and node.parent == node.parent.parent.right:
                self._left_rotate(node.parent.parent)
                self._left_rotate(node.parent)
            # Zig-Zag case
            elif node == node.parent.right and node.parent == node.parent.parent.left:
                self._left_rotate(node.parent)
                self._right_rotate(node.parent)
            else: # node == node.parent.left and node.parent == node.parent.parent.right
                self._right_rotate(node.parent)
                self._left_rotate(node.parent)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        Performs the splaying operation on the found node. If the node is not
        found, it splays the last accessed node (the would-be parent) instead.
        
        Args:
            key: The integer key to search for.
            
        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        last_visited = self.root
        current = self.root
        while current:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:  # Key found
                self._splay(current)
                return True
        
        # Key not found, splay the last visited node (parent)
        self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, it is splayed to the root. If the key is new,
        it is inserted and then splayed to the root.
        
        Args:
            key: The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Search for the key, which also splays the tree
        if self.search(key):
            return # Key already exists, it's now the root

        # After search(key) fails, the root is the closest key.
        # We can now insert the new key relative to this new root.
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
        else: # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None
        
        self.root.parent = new_node
        self.root = new_node


    def delete(self, key):
        """
        Deletes a key from the tree.
        
        Args:
            key: The integer key to delete.
        """
        # Search for the key, this will splay it to the root if it exists
        if not self.search(key):
            return # Key not in tree

        # At this point, the node to delete is the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Find the maximum element in the left subtree
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Splay this maximum element to the root of the left subtree
            self._splay(max_in_left)
            
            # The new root of the tree is the splayed max element
            self.root = max_in_left
            self.root.parent = None # It's the new root
            
            # Attach the original right subtree
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root

    # Helper method for visualization/testing
    def in_order_traversal(self):
        """Returns a list of keys in in-order."""
        result = []
        self._in_order_recursive(self.root, result)
        return result

    def _in_order_recursive(self, node, result):
        if node:
            self._in_order_recursive(node.left, result)
            result.append(node.key)
            self._in_order_recursive(node.right, result)