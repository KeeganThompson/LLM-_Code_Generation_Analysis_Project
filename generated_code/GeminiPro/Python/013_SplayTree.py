import sys

class SplayTree:
    """
    A self-contained Splay Tree class that implements a dictionary-like set for integers.
    
    This implementation includes methods for insertion, deletion, and searching.
    The key feature is the splaying operation, which moves recently accessed
    nodes to the root of thetree to optimize for future accesses.
    """

    class _Node:
        """A private nested class to represent a node in the Splay Tree."""
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

    def _right_rotate(self, y):
        """Performs a right rotation on node y."""
        x = y.left
        y.left = x.right
        if x.right:
            x.right.parent = y
            
        x.parent = y.parent
        if not y.parent:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
            
        x.right = y
        y.parent = x

    def _splay(self, node):
        """
        Performs the splaying operation on a node, moving it to the root.
        Splaying involves a sequence of rotations (Zig, Zig-Zig, Zig-Zag)
        until the node becomes the root.
        """
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            
            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree.
        
        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node (the potential parent) 
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
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Key not found, splay the last visited node if the tree was not empty
        if last_node:
            self._splay(last_node)
            
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.
        
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
                # Key already exists, splay it and we're done
                self._splay(node)
                return

        # Create and insert the new node
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
        
        This operation first splays the node to be deleted (if it exists) to the
        root. Then, the root is removed, and the remaining left and right
        subtrees are joined. The joining process involves splaying the maximum
        element of the left subtree to its root before attaching the right subtree.
        
        Args:
            key (int): The integer key to delete.
        """
        # Splay the node with the given key to the root. If not found,
        # the closest node is splayed. search() handles this.
        if not self.search(key):
            # Key not in the tree, nothing to delete.
            # search() has already splayed the last accessed node.
            return

        # Now, the node to be deleted is at the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree from the old root
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Make the left subtree the temporary main tree and splay its max node.
            # This makes max_node the new root of the combined left subtree,
            # and crucially, it will have no right child.
            self.root = left_subtree
            self._splay(max_node)
            
            # self.root is now max_node. Attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root