import sys

class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.

    This class provides a dictionary-like set for storing unique integers.
    It supports insertion, deletion, and searching operations. The key feature
    is the splaying operation: whenever a key is accessed (searched, inserted,
    or deleted), the corresponding node is moved to the root of the tree to
    optimize for future accesses.
    """

    class _Node:
        """A private inner class representing a node in the Splay Tree."""
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
            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left:
                if parent == grandparent.left:  # Zig-zig case (left-left)
                    self._right_rotate(grandparent)
                    self._right_rotate(parent)
                else:  # Zig-zag case (left-right)
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)
            else:  # node is right child
                if parent == grandparent.right:  # Zig-zig case (right-right)
                    self._left_rotate(grandparent)
                    self._left_rotate(parent)
                else:  # Zig-zag case (right-left)
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.

        If the key is found, the node containing the key is splayed to the root.
        If the key is not found, the last accessed node (the parent of where
        the key would have been) is splayed to the root.

        Args:
            key (int): The key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
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
        
        # Key not found, splay the last accessed node
        self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key (int): The key to insert.
        """
        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay the node and return
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

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
        Deletes a key from the tree.

        The standard splay tree deletion algorithm is used:
        1. Search for the key, which brings the node to the root.
        2. If found, remove the root and join the two resulting subtrees.
           The join operation involves splaying the maximum element of the
           left subtree to its root and then attaching the right subtree.

        Args:
            key (int): The key to delete.
        """
        # Search for the key. This brings the node to the root if it exists,
        # or the last-accessed node if it doesn't.
        self.search(key)

        # If the root is None or its key doesn't match, the key wasn't in the tree.
        if not self.root or self.root.key != key:
            return

        # The node to delete is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # If there is a left subtree, we make its largest element the new root.
            # 1. Disconnect the left subtree from the old root.
            left_subtree.parent = None
            
            # 2. Find the node with the maximum key in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # 3. Splay this maximum node to the root of the left subtree.
            # We temporarily set self.root to the left subtree's root to use our
            # existing _splay implementation, which operates on self.root.
            self.root = left_subtree
            self._splay(max_node)
            
            # 4. After splaying, self.root is max_node. Now, attach the original
            # right subtree as its right child.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root