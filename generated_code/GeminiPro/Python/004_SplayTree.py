class SplayTree:
    """
    A complete, self-contained Python class that implements a Splay Tree.

    This tree functions as a dictionary-like set for storing unique integer keys.
    The core operations (search, insert, delete) all utilize a "splaying"
    action. This moves the node that was accessed (or its parent if the node
    was not found) to the root of the tree. This self-optimizing behavior
    positions frequently accessed elements closer to the root, improving
    average-case performance for non-uniform access patterns.
    """

    class _Node:
        """A private helper class representing a node in the splay tree."""
        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation around node x."""
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

    def _right_rotate(self, y):
        """Performs a right rotation around node y."""
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
        x.right = y
        y.parent = x

    def _splay(self, node):
        """
        Performs the splaying operation on a node, moving it to the root.
        This is the core mechanism of the Splay Tree.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case: Parent is the root
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:
                # Zig-Zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:
                # Zig-Zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last non-null node accessed during the
        search (the would-be parent) is splayed to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = None
        while current:
            last_visited = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node to the root.
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted as a new node, which is then splayed
        to the root.

        Args:
            key (int): The integer key to insert.
        """
        # 1. Handle the case of an empty tree
        if not self.root:
            self.root = self._Node(key)
            return

        # 2. Search for the key. If it exists, splay that node and finish.
        # If not, find the parent where the key should be inserted.
        current = self.root
        parent = None
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and we are done.
                self._splay(current)
                return
        
        # 3. The key was not found. Splay the parent (last visited node).
        self._splay(parent)

        # 4. Now, the root is the closest key to the one we want to insert.
        # We split the tree and insert the new key as the new root.
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.left = self.root.left
            new_node.right = self.root
            if new_node.left:
                new_node.left.parent = new_node
            self.root.parent = new_node
            self.root.left = None
        else:  # key > self.root.key
            new_node.right = self.root.right
            new_node.left = self.root
            if new_node.right:
                new_node.right.parent = new_node
            self.root.parent = new_node
            self.root.right = None
        
        self.root = new_node
        self.root.parent = None

    def delete(self, key):
        """
        Deletes a key from the tree.

        After deletion, the parent of the removed node is splayed to the root.
        If the key is not found, the last accessed node is splayed.

        Args:
            key (int): The integer key to delete.
        """
        # 1. Use search to find the key and splay it (or its parent) to the root.
        if not self.search(key):
            # Key not found. search() already splayed the closest node.
            return

        # 2. If search returned True, the node to delete is now the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # If a left subtree exists, we need to merge it with the right one.
            # We find the maximum element in the left subtree, splay it to the
            # root of the left subtree, and then attach the right subtree.
            left_subtree.parent = None
            
            # Find the maximum node in the (now detached) left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node to the root of its subtree.
            # We temporarily set self.root to perform the splay within the subtree.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, self.root is max_node. Attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root

    def __str__(self):
        """Returns an in-order traversal string representation of the tree."""
        if not self.root:
            return "[]"
        return str(self._in_order(self.root))

    def _in_order(self, node):
        """Helper for recursive in-order traversal."""
        if not node:
            return []
        return self._in_order(node.left) + [node.key] + self._in_order(node.right)