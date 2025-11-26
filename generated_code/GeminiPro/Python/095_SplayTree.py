import sys

# It's good practice to set a higher recursion limit for tree-based structures,
# though this specific implementation is iterative and doesn't rely on deep recursion.
sys.setrecursionlimit(2000)

class SplayTree:
    """
    A complete, self-contained Splay Tree class that implements a
    dictionary-like set for storing unique integer keys.

    This implementation provides `insert`, `delete`, and `search` methods.
    A key characteristic of a Splay Tree is that any accessed node (through
    search, insertion, or deletion) is moved to the root of the tree using a
    series of rotations. This "splaying" operation provides amortized
    logarithmic time complexity for all operations, making the tree
    self-optimizing by keeping frequently accessed nodes near the top.
    """

    class _Node:
        """A private helper class representing a node in the Splay Tree."""
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
        Splays the node x to the root of the tree through a series of rotations.
        """
        while x.parent:
            parent = x.parent
            grandparent = parent.parent
            if not grandparent:
                # Zig case
                if x == parent.left:
                    self._right_rotate(parent)
                else:
                    self._left_rotate(parent)
            elif x == parent.left and parent == grandparent.left:
                # Zig-Zig case (left-left)
                self._right_rotate(grandparent)
                self._right_rotate(parent)
            elif x == parent.right and parent == grandparent.right:
                # Zig-Zig case (right-right)
                self._left_rotate(grandparent)
                self._left_rotate(parent)
            elif x == parent.right and parent == grandparent.left:
                # Zig-Zag case (left-right)
                self._left_rotate(parent)
                self._right_rotate(grandparent)
            else:
                # Zig-Zag case (right-left)
                self._right_rotate(parent)
                self._left_rotate(grandparent)

    def search(self, key):
        """
        Searches for a key and splays the accessed node to the root.

        If the key is found, the node with that key is splayed. If not found,
        the last non-null node accessed during the search is splayed.

        Args:
            key (int): The integer key to search for.

        Returns:
            bool: True if the key is found in the tree, False otherwise.
        """
        if not self.root:
            return False

        current_node = self.root
        last_node = self.root
        while current_node:
            last_node = current_node
            if key == current_node.key:
                self._splay(current_node)
                return True
            elif key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        
        # Splay the last accessed node if the key was not found.
        self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a new integer key into the tree.

        If the key does not exist, it is inserted and the new node is splayed
        to the root. If the key already exists, the existing node is splayed
        to the root.

        Args:
            key (int): The integer key to insert.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        # Use search to find the key. If it exists, search will splay it.
        if self.search(key):
            return

        # If key is not found, search() has splayed the closest node to the root.
        # Now, we insert the new key as the new root and restructure.
        new_node = self._Node(key)
        
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
            if new_node.left:
                new_node.left.parent = new_node
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
            if new_node.right:
                new_node.right.parent = new_node
        
        self.root.parent = new_node
        self.root = new_node

    def delete(self, key):
        """
        Deletes an integer key from the tree.

        First, the tree is searched for the key, which brings the node (or its
        closest neighbor) to the root. If the key is present at the root, it is
        removed, and its two subtrees are joined.

        Args:
            key (int): The integer key to delete.
        """
        # Splay the node to the root. If not found, splay the closest node.
        if not self.search(key):
            # Key is not in the tree, nothing to delete.
            return

        # After search, the node to delete is at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect the left subtree to operate on it.
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max_node. It will become the root of the left subtree.
            # After splaying, it will have no right child.
            # We use a temporary SplayTree instance to perform the splay
            # on the disconnected subtree.
            temp_tree = SplayTree()
            temp_tree.root = left_subtree
            temp_tree._splay(max_node)
            
            # The new root of the main tree is the splayed max_node.
            self.root = temp_tree.root
            
            # Attach the original right subtree to the new root.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root