class SplayTree:
    """
    A complete, self-contained Splay Tree class that implements a
    dictionary-like set for integers.

    This implementation includes insert, delete, and search methods. The core
    feature of a splay tree is its self-optimizing nature: frequently accessed
    nodes are moved closer to the root, leading to amortized logarithmic time
    complexity for its operations.
    """

    class _Node:
        """A private helper class for the nodes of the splay tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root = None

    def _left_rotate(self, x):
        """Performs a left rotation on the subtree rooted at node x."""
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
        """Performs a right rotation on the subtree rooted at node x."""
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

    def _splay(self, node):
        """
        Performs the splaying operation on a node, moving it to the root.
        Splaying involves a sequence of rotations (Zig, Zig-Zig, Zig-Zag)
        until the node is the root of the tree.
        """
        if not node:
            return
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig step
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag (node is left child, parent is right child)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.

        Performs the splaying operation on the accessed node if the key is found,
        or on the last accessed node (the parent of the potential location) if
        the key is not found.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise. After the operation,
            the splayed node will be the new root of the tree.
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
        
        # Key not found, splay the last accessed node to the root.
        self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then the new node is splayed
        to the root, becoming the new root.

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
                # Key already exists, splay it to the root and we're done.
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Insert the new node as a child of the last-visited node.
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the newly inserted node to the root.
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The node containing the key is first splayed to the root and then removed.
        The tree is then restructured by joining the remaining left and right
        subtrees. If the key is not found, the last-accessed node in the search
        path is splayed to the root.

        Args:
            key: The integer key to delete.
        """
        # Splay the node with the given key (or its would-be parent) to the root.
        if not self.search(key):
            # Key was not found. search() has already splayed the last-accessed node.
            return

        # After search(), if the key was found, it is now at the root.
        # This check is slightly redundant due to the search above, but is safe.
        if not self.root or self.root.key != key:
            return

        # The node to delete is at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # If there is a left subtree, find its maximum element.
            # This maximum element will become the new root of the combined tree.
            left_subtree.parent = None  # Temporarily detach the left subtree.
            
            # Find the maximum node in the (now separate) left subtree.
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Splay this maximum node to the root of the left subtree.
            # We temporarily set self.root to perform the splay within this subtree.
            self.root = left_subtree
            self._splay(max_in_left)  # After this, self.root is max_in_left.
            
            # The new root's right child is the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root