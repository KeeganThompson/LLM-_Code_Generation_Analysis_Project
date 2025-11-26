class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.

    This implementation includes methods for insertion, deletion, and searching.
    The key feature of a splay tree is that recently accessed elements are moved
    to the root of the tree to optimize for future accesses.
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
        """Performs a left rotation on the given node x."""
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
        """Performs a right rotation on the given node x."""
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
        Performs the splay operation on node x, moving it to the root.
        """
        while x.parent:
            p = x.parent
            g = p.parent  # Grandparent
            if not g:
                # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:
                # Zig-Zig case (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:
                # Zig-Zig case (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:
                # Zig-Zag case (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:
                # Zig-Zag case (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

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
                # Key found
                self._splay(node)
                return True

        # Key not found, splay the last visited node
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key does not exist, it is inserted and the new node is splayed
        to the root. If the key already exists, the existing node is splayed
        to the root.

        Args:
            key (int): The integer key to insert.
        """
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                # Key already exists, splay it and return
                self._splay(node)
                return

        # Insert the new node
        new_node = self._Node(key)
        new_node.parent = parent
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The deletion process involves splaying the node to the root, removing it,
        and then joining the remaining left and right subtrees.

        Args:
            key (int): The integer key to delete.
        """
        # Search for the key, which splays the node (or its parent) to the root
        if not self.search(key):
            # Key is not in the tree, search() already splayed the closest node.
            return

        # After search, if the key was found, it's at the root.
        # The check self.root.key == key is implicitly true here because search() returned True.
        
        z = self.root
        left_subtree = z.left
        right_subtree = z.right

        # Disconnect subtrees from the root
        if left_subtree:
            left_subtree.parent = None
        if right_subtree:
            right_subtree.parent = None

        # Join the subtrees
        if not left_subtree:
            self.root = right_subtree
        else:
            # Find the maximum element in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to the root of the left subtree
            # We can do this by temporarily setting the root and calling splay
            self.root = left_subtree
            self._splay(max_node)

            # After splaying, self.root is max_node.
            # max_node has no right child. Attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root