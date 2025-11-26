import sys

class SplayTree:
    """
    A self-contained Python class implementing a Splay Tree.

    This class provides a dictionary-like set for storing unique integer keys.
    It supports insert, delete, and search operations. The key feature is the
    splaying operation performed on each access, which moves the accessed
    node (or its parent if the node is not found) to the root of the tree.
    This amortizes the cost of operations to O(log n).
    """

    class _Node:
        """
        A private inner class representing a node in the Splay Tree.
        """
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """
        Initializes an empty Splay Tree.
        """
        self.root = None

    def _left_rotate(self, x):
        """
        Performs a left rotation on the given node x.
        """
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
        """
        Performs a right rotation on the given node x.
        """
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
        Performs the splaying operation on the given node, moving it to the root.
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

        If the key is found, the corresponding node is splayed to the root
        and True is returned.
        If the key is not found, the last accessed node (the would-be parent)
        is splayed to the root and False is returned.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        last_visited = None
        current = self.root
        while current:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found, splay the node and return True
                self._splay(current)
                return True
        
        # Key not found, splay the last visited node (parent) if it exists
        if last_visited:
            self._splay(last_visited)
        
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
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
        
        # Insert the new node
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        The operation first searches for the key, which splays the node (or its
        parent) to the root. If the key is found at the root, it is removed,
        and the remaining subtrees are joined.

        Args:
            key (int): The integer key to delete.
        """
        # Search for the key. This will splay the node or its parent to the root.
        if not self.search(key):
            # Key not in the tree. search() already splayed the would-be parent.
            return

        # After search, if the key was found, it is now at the root.
        node_to_delete = self.root
        
        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        elif not right_subtree:
            # No right child, the left subtree becomes the new tree.
            self.root = left_subtree
            if left_subtree:
                left_subtree.parent = None
        else:
            # Both children exist.
            # 1. Detach the left subtree.
            left_subtree.parent = None
            
            # 2. Find the maximum node in the left subtree.
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # 3. Splay this maximum node to the root of the left subtree.
            #    Temporarily make the left subtree the main tree to use _splay.
            self.root = left_subtree
            self._splay(max_in_left)
            
            # 4. The new root (max_in_left) now has the right_subtree as its
            #    right child. By property, it has no right child before this.
            self.root.right = right_subtree
            right_subtree.parent = self.root