class SplayTree:
    """
    An implementation of a dictionary-like set for integers using a Splay Tree.

    This data structure provides logarithmic amortized time complexity for
    insert, delete, and search operations. The key feature is the splaying
    operation, which moves accessed elements to the root of the tree to
    optimize for future accesses.
    """

    class _Node:
        """A node in the Splay Tree."""
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
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
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

        Performs the splaying operation on the accessed node if found,
        or on its would-be parent if not found.

        Args:
            key (int): The key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
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
                # Key found, splay the node and return True
                self._splay(node)
                return True

        # Key not found, splay the last visited node (the parent)
        if last_visited:
            self._splay(last_visited)

        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.

        Args:
            key (int): The key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key already exists, splay the found node
                self._splay(node)
                return

        # Insert the new node
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The standard splay tree deletion algorithm is used:
        1. Search for the key, which splays the node to the root.
        2. If found, remove the root and join the two resulting subtrees.
           - The largest element of the left subtree is splayed to its root.
           - The right subtree is then attached as the right child of this new root.

        Args:
            key (int): The key to delete.
        """
        # Splay the node with the key (or its parent) to the root
        if not self.search(key):
            # The search method returns False if key is not found.
            # It also splays the closest node, so the tree is already restructured.
            return

        # If search returned True, the key is now at the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Make the left subtree the main tree temporarily
            left_subtree.parent = None
            self.root = left_subtree

            # Find the maximum node in the (now main) left subtree
            max_node = self.root
            while max_node.right:
                max_node = max_node.right

            # Splay this max node. It becomes the new root of the combined tree.
            self._splay(max_node)

            # Attach the original right subtree
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root