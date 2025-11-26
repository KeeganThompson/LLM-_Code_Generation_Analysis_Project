import sys

# It's recommended to increase recursion limit for deep trees, though splaying mitigates this.
# sys.setrecursionlimit(2000)

class SplayTree:
    """
    Implements a splay tree for storing unique integers.

    This data structure behaves like a set and supports insert, delete, and search operations.
    The key feature is that any accessed (searched, inserted, or deleted) node
    is moved to the root of the tree through a series of rotations,
    a process called "splaying". This keeps frequently accessed elements
    near the top for faster subsequent access.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty splay tree."""
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
        Splays the given node to the root of the tree.
        """
        while node.parent:
            p = node.parent
            gp = p.parent
            if not gp:  # Zig case
                if node == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif node == p.left and p == gp.left:  # Zig-Zig case (left-left)
                self._right_rotate(gp)
                self._right_rotate(p)
            elif node == p.right and p == gp.right:  # Zig-Zig case (right-right)
                self._left_rotate(gp)
                self._left_rotate(p)
            elif node == p.right and p == gp.left:  # Zig-Zag case (left-right)
                self._left_rotate(p)
                self._right_rotate(gp)
            else:  # Zig-Zag case (right-left)
                self._right_rotate(p)
                self._left_rotate(gp)

    def search(self, key):
        """
        Searches for a key in the splay tree.

        Performs the splaying operation on the accessed node if found,
        or on its would-be parent if not found.

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
        
        # Key not found. Splay the last visited node (the parent) if it exists.
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the splay tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and then the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        # Find position for new node, similar to BST insert
        parent = None
        current = self.root
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and we are done
                self._splay(current)
                return

        # Create the new node
        new_node = self._Node(key)
        new_node.parent = parent

        if not parent:
            # The tree was empty
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the splay tree.

        The node (if found) is first splayed to the root, then removed.
        If the key is not found, the last accessed node in the search path is splayed.

        Args:
            key: The integer key to delete.
        """
        # Splay the node with the key (or its parent) to the root
        if not self.search(key):
            # Key not in the tree. search() already splayed the closest node.
            return

        # At this point, the node to delete is the root because search(key) found it
        # and splayed it.
        z = self.root
        
        left_subtree = z.left
        right_subtree = z.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # No right child, so the left subtree becomes the new tree.
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both children exist. We need to join the left and right subtrees.
            # 1. Make the left subtree the main tree temporarily.
            left_subtree.parent = None
            self.root = left_subtree

            # 2. Find the maximum element in this new tree (the new root).
            max_node = self.root
            while max_node.right:
                max_node = max_node.right

            # 3. Splay this maximum element to the root.
            #    After this, self.root will be max_node, and it has no right child.
            self._splay(max_node)

            # 4. Attach the original right subtree as the right child of the new root.
            self.root.right = right_subtree
            right_subtree.parent = self.root