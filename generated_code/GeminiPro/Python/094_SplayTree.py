import sys

class SplayTree:
    """
    A self-contained Python class that implements a dictionary-like set for
    integers using a Splay Tree.

    The main public methods are:
    - insert(key): Adds a key to the tree.
    - delete(key): Removes a key from the tree.
    - search(key): Searches for a key and splays the accessed node.
    """

    class _Node:
        """A private inner class representing a node in the Splay Tree."""
        def __init__(self, key, parent=None):
            self.key = key
            self.parent = parent
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

    def _splay(self, x):
        """
        Performs the splay operation on node x, moving it to the root.
        """
        while x.parent:
            p = x.parent
            g = p.parent

            if not g:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree.

        This method performs the splaying operation on the accessed node (if the
        key is found) or its parent (if the key is not found) to move it to
        the root.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        node = self.root
        last_node = self.root
        found = False
        
        while node:
            last_node = node
            if key == node.key:
                found = True
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Splay the last accessed node (or the found node) to the root
        self._splay(last_node)
        
        return found

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the
        root. If the key is new, it is inserted as in a standard BST, and
        the new node is then splayed to the root.

        Args:
            key (int): The integer key to insert.
        """
        # Case 1: The tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Traverse the tree to find the insertion point or an existing key
        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay it and we are done
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Case 2: Key not found, insert a new node
        new_node = self._Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.

        If the key is not found, the tree is splayed based on the last
        accessed node during the search, and no deletion occurs. If the key
        is found, it is removed, and the tree is restructured.

        Args:
            key (int): The integer key to delete.
        """
        # Search for the key. If found, it will be splayed to the root.
        if not self.search(key):
            # Key is not in the tree, nothing to delete.
            # search() has already splayed the closest node.
            return

        # At this point, the node to delete is the root due to search()
        node_to_delete = self.root
        
        left_subtree = node_to_delete.left
        right_subtree = node_to_delete.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree from the old root
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max element to the root of the left subtree.
            # We temporarily set self.root to the left subtree's root to
            # perform the splay operation within that subtree.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, self.root is the new root of the combined tree.
            # It has no right child, so we attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root