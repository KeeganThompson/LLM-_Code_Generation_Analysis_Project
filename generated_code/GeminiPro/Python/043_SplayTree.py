class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.

    This implementation includes insert, delete, and search operations. The key
    feature of a splay tree is that recently accessed elements are moved to the
    root of the tree to optimize for temporal locality of reference, providing
    amortized O(log n) time complexity for its operations.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key, parent=None, left=None, right=None):
            self.key = key
            self.parent = parent
            self.left = left
            self.right = right

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
            # x was the root, y is the new root
            # Note: self.root is not updated here; the caller is responsible.
            pass
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
            # x was the root, y is the new root
            # Note: self.root is not updated here; the caller is responsible.
            pass
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

        Returns the new root of the splayed tree (which is x).
        """
        if not x:
            return None
            
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig step
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:
                # Zig-Zig (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:
                # Zig-Zig (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:
                # Zig-Zag (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:
                # Zig-Zag (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)
        return x

    def search(self, key):
        """
        Searches for a key in the tree.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the would-be parent)
        is splayed to the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key found, splay the node
                self.root = self._splay(node)
                return True

        # Key not found. If the tree was not empty, splay the last visited node.
        if last_node:
            self.root = self._splay(last_node)
            
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        # Case 1: Tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Case 2: Tree is not empty, find insertion point
        current = self.root
        parent = None
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay the found node and we are done.
                self.root = self._splay(current)
                return

        # Insert the new node
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node
        self.root = self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        This is done by splaying the node to the root, removing it, and then
        joining the two resulting subtrees.

        Args:
            key (int): The integer key to delete.
        """
        # First, search for the key. This will splay the node if it exists,
        # or a nearby node if it doesn't.
        if not self.search(key):
            # Key is not in the tree, and search() has already splayed the
            # last accessed node. Nothing more to do.
            return

        # After search, if the key was found, it's now at the root.
        # self.root.key will be equal to key.
        
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # The left subtree exists. We will make its largest element the new root.
            # Detach the left subtree to work on it independently.
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree.
            new_root = left_subtree
            while new_root.right:
                new_root = new_root.right
            
            # Splay this maximum element to the root of the left subtree.
            # After this, new_root will be the root and have no right child.
            new_root = self._splay(new_root)

            # Join the original right subtree to the new root.
            new_root.right = right_subtree
            if right_subtree:
                right_subtree.parent = new_root
            
            self.root = new_root