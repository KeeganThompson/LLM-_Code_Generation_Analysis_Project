class SplayTree:
    """
    A complete, self-contained Python class that implements a dictionary-like set
    for integers using a Splay Tree.

    The main operations are insert, delete, and search. Any access to a node
    (or a would-be node) causes a "splay" operation, which moves the accessed
    node (or its parent) to the root of the tree. This restructuring helps to
    maintain an amortized O(log n) time complexity for all operations.
    """

    class Node:
        """
        An inner class representing a node in the Splay Tree.
        Each node stores a key and pointers to its left child, right child,
        and parent, which are essential for the rotation and splaying logic.
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
        """
        Performs a left rotation on the given node x.
        This operation is a fundamental building block for splaying.
        """
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
        """
        Performs a right rotation on the given node x.
        This operation is a fundamental building block for splaying.
        """
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
        Performs the splay operation on a node, moving it to the root
        through a series of rotations. The type of rotation (Zig, Zig-Zig,
        or Zig-Zag) depends on the configuration of the node, its parent,
        and its grandparent.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig case
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig case
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag case
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (node is left child, parent is right child)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree and performs the splaying operation.

        If the key is found, the corresponding node is splayed to the root, and
        the method returns True. If the key is not found, the last non-null node
        visited during the search (the would-be parent of the key) is splayed
        to the root, and the method returns False.

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
        
        # Key not found, splay the last visited node to the root
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        This method follows the standard bottom-up insertion for Splay Trees.
        It first performs a regular Binary Search Tree insertion. Then, the
        newly inserted node is splayed to the root. If the key already exists,
        the existing node is splayed to the root and no new node is inserted.

        Args:
            key (int): The integer key to insert.
        """
        # Find parent for new node using standard BST logic
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

        # Create and link the new node
        new_node = self.Node(key)
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
        Deletes a key from the tree.

        First, the key is searched for, which brings the node (or its would-be
        parent) to the root. If the key is found at the root, the tree is split
        into two subtrees (left and right). The maximum element of the left
        subtree is then found, splayed to the root of the left subtree, and
        the right subtree is attached as its right child.

        Args:
            key (int): The integer key to delete.
        """
        # Search for the key. This splays the node (if found) or its
        # would-be parent to the root.
        if not self.search(key):
            # Key not in the tree. search() has already splayed the last
            # visited node. Nothing more to do.
            return

        # If search returned true, the node to delete is now at the root.
        z = self.root
        left_subtree = z.left
        right_subtree = z.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # The left subtree exists. We will make the maximum element of the
            # left subtree the new root of the combined tree.
            
            # Isolate the left subtree to perform a splay within it.
            left_subtree.parent = None
            
            # Find the max node in the now-isolated left subtree.
            new_root_candidate = left_subtree
            while new_root_candidate.right:
                new_root_candidate = new_root_candidate.right
            
            # Splay the max node to the top of its subtree.
            # We can do this by temporarily making that subtree the main tree.
            self.root = left_subtree
            self._splay(new_root_candidate)
            
            # After splaying, `self.root` is the root of the splayed left
            # subtree (the max node). We re-attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root