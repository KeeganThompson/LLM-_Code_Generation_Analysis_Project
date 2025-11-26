class SplayTree:
    """
    A complete, self-contained Splay Tree class that implements a
    dictionary-like set for integers.

    This data structure provides amortized O(log n) time complexity for search,
    insert, and delete operations. The key feature is the splaying operation,
    which moves frequently accessed elements closer to the root of the tree.
    """

    class _Node:
        """A private helper class for the nodes of the tree."""
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
        """Performs a right rotation on node x."""
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

    def _splay(self, x):
        """
        Performs the splaying operation on node x, moving it to the root.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:  # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left:
                if parent == grandparent.left:  # Zig-Zig case
                    self._right_rotate(grandparent)
                    self._right_rotate(parent)
                else:  # Zig-Zag case
                    self._right_rotate(parent)
                    self._left_rotate(grandparent)
            else: # x is right child
                if parent == grandparent.right:  # Zig-Zig case
                    self._left_rotate(grandparent)
                    self._left_rotate(parent)
                else:  # Zig-Zag case
                    self._left_rotate(parent)
                    self._right_rotate(grandparent)

    def insert(self, key):
        """
        Inserts a key into the splay tree.
        If the key already exists, the node is splayed to the root.
        """
        node = self.root
        parent = None
        
        while node:
            parent = node
            if key == node.key:
                # Key already exists, splay it and we are done
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        new_node = self._Node(key)
        new_node.parent = parent
        
        if not parent:
            self.root = new_node  # Tree was empty
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
            
        # Splay the newly inserted node to the root
        self._splay(new_node)

    def search(self, key):
        """
        Searches for a key in the splay tree.
        
        Performs the splaying operation on the accessed node (if found) or
        its parent (if not found) to move it to the root.

        Returns:
            bool: True if the key is found, False otherwise.
        """
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
        
        # If key is not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
            
        return False

    def delete(self, key):
        """
        Deletes a key from the splay tree.
        If the key is not found, the tree is splayed based on the search path.
        """
        # Splay the node with the key (or its would-be parent) to the root
        if not self.search(key):
            # Key was not found. search() already splayed the last accessed node.
            return
        
        # At this point, the node to delete is the root, and we know it exists
        # because search() would have returned False otherwise.
        if self.root.key != key:
            return

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, promote the right subtree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        elif not right_subtree:
            # No right child, promote the left subtree
            self.root = left_subtree
            if left_subtree:
                left_subtree.parent = None
        else:
            # Both children exist. Join the two subtrees.
            left_subtree.parent = None # Disconnect for now
            
            # Find the maximum element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to be the root of the left subtree.
            # We can do this by temporarily setting self.root to the left
            # subtree and then calling our existing _splay method.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, max_node is the new root (self.root).
            # It's guaranteed to not have a right child.
            # Attach the original right subtree.
            self.root.right = right_subtree
            right_subtree.parent = self.root