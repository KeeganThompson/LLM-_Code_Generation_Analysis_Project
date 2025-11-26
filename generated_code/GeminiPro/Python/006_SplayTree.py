import sys

class SplayTree:
    """
    A self-contained Python class that implements a splay tree for integers.
    This class provides a dictionary-like set interface with insert, delete,
    and search methods. The key feature is the splaying operation, which
    moves frequently accessed elements to the root of the tree to optimize
    future lookups.
    """

    class _Node:
        """A node in the Splay Tree, nested within the SplayTree class."""
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
        """Moves a given node to the root of the tree using splay operations."""
        if not node:
            return
        
        while node.parent:
            parent = node.parent
            grandparent = parent.parent
            
            if not grandparent:  # Zig case
                if node == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif node == parent.left and parent == grandparent.left:  # Zig-Zig case (Left-Left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif node == parent.right and parent == grandparent.right:  # Zig-Zig case (Right-Right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif node == parent.right and parent == grandparent.left:  # Zig-Zag case (Left-Right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:  # Zig-Zag case (Right-Left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key in the tree and splays the accessed node.
        
        If the key is found, its node is splayed to the root. If not found,
        the last non-null node on the search path is splayed to the root.
        
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
        
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key is new, it is inserted and the new node is splayed to the root.
        If the key already exists, the corresponding node is splayed to the root.
        
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
            if key == current.key:
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        This operation first splays the node (or its would-be parent) to the root.
        If the key is found at the root, it is removed and the two resulting
        subtrees are joined.
        
        Args:
            key (int): The integer key to delete.
        """
        if not self.search(key):
            # Key not found; search() already splayed the last accessed node.
            return

        # After search(), if the key was found, it is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            left_subtree.parent = None
            
            # Find the max node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right

            # Splay this max node to the root of the (now separate) left subtree.
            # This is done by temporarily making the left subtree the main tree.
            self.root = left_subtree
            self._splay(max_node)
            
            # The new root (the splayed max_node) now becomes the root of the whole tree.
            # Its right child is set to the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root