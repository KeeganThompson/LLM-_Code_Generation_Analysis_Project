class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.

    This class provides a dictionary-like set for integers, supporting
    insert, delete, and search operations. The key feature is the splaying
    operation, which moves accessed nodes to the root to optimize
    future accesses.
    """

    class _Node:
        """A private inner class for the nodes of the Splay Tree."""
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

    def _splay(self, node):
        """
        Performs the splay operation on a node, moving it to the root.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig step
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig step
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig step
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            else:  # Zig-Zag step
                if node == parent.right and parent == grandparent.left:
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)
                else:
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        Performs a splay operation on the found node or the last accessed
        node if the key is not found.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        last_visited = None
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
        
        # Key not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
        
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node is splayed to the root.
        If the key does not exist, it is inserted and then splayed to the root.

        Args:
            key: The integer key to insert.
        """
        # Case 1: Tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the closest node to the key. If key exists, it becomes the root.
        if self.search(key):
            return  # Key already exists, search has splayed it.

        # After a failed search, the root is the closest leaf/node.
        # We insert the new key as the new root and restructure.
        new_node = self._Node(key)
        old_root = self.root

        if key < old_root.key:
            new_node.right = old_root
            new_node.left = old_root.left
            if old_root.left:
                old_root.left.parent = new_node
            old_root.left = None
        else:  # key > old_root.key
            new_node.left = old_root
            new_node.right = old_root.right
            if old_root.right:
                old_root.right.parent = new_node
            old_root.right = None
        
        old_root.parent = new_node
        self.root = new_node

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is found, it is deleted. The tree is then restructured
        by splaying the largest element in the left subtree. If the key is
        not found, the tree structure is modified by the preceding search
        and splay operation.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. This will splay it to the root if it exists.
        if not self.search(key):
            # Key is not in the tree, nothing to delete.
            # search() has already splayed the closest node.
            return

        # At this point, the node to delete is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree from the old root.
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node. To do this within the left subtree,
            # we temporarily set it as the main root.
            self.root = left_subtree
            self._splay(max_node)
            
            # The splayed max_node is now the root. It has no right child.
            # Attach the original right subtree to it.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root