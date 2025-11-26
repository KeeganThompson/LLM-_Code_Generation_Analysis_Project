class SplayTree:
    """
    A complete, self-contained Splay Tree class that implements a
    dictionary-like set for storing unique integer keys.

    This implementation includes the required methods: insert(key), delete(key),
    and search(key). The splaying operation is central to all these methods,
    ensuring that frequently accessed elements are moved closer to the root
    to optimize future access times.
    """

    class _Node:
        """
        A private inner class representing a node in the splay tree.
        Each node stores a key and references to its parent, left child,
        and right child.
        """
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

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

    def _splay(self, x):
        """
        Performs the splaying operation on node x, moving it to the root.
        This operation consists of a sequence of rotations (Zig, Zig-Zig,
        or Zig-Zag) until x becomes the root of the tree.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig step
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-zig step (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-zig step (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-zag step (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-zag step (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, its node is splayed to the root, and True is returned.
        If the key is not found, the last accessed node (the one that would be
        the parent of the key if it existed) is splayed to the root, and False
        is returned.

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
                self._splay(node)
                return True
        
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the splay tree.

        If the key does not exist, it is inserted as a new node, and this new
        node is splayed to the root. If the key already exists, the node
        containing that key is splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        parent = None
        current = self.root
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay the node and return
                self._splay(current)
                return

        new_node = self._Node(key)
        new_node.parent = parent

        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the splay tree.

        First, the key is searched, which brings the node with the key (or the
        closest node if not found) to the root. If the key is present at the
        root, it is removed. The remaining left and right subtrees are then
        merged back into a single tree.

        Args:
            key (int): The integer key to delete.
        """
        if not self.root:
            return

        # Search for the key, this will splay the node or its parent to the root
        self.search(key)
        
        # If the key is not at the root after splaying, it wasn't in the tree
        if self.root.key != key:
            return

        # The node to delete is now the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        elif not right_subtree:
            self.root = left_subtree
            if left_subtree:
                left_subtree.parent = None
        else:
            # Both subtrees exist; merge them
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node_in_left = left_subtree
            while max_node_in_left.right:
                max_node_in_left = max_node_in_left.right
            
            # Splay this max node to the root of the left subtree.
            # We can do this by temporarily treating the left subtree as the main tree.
            self.root = left_subtree
            self._splay(max_node_in_left)
            
            # After splaying, self.root is max_node_in_left. It has no right child.
            # Attach the original right subtree as its new right child.
            self.root.right = right_subtree
            right_subtree.parent = self.root