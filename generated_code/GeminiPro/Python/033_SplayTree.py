import sys
from typing import Optional

# A higher recursion limit can be useful for deep tree structures,
# though this splay tree implementation is iterative.
# It is included as a safeguard for potential alternative recursive helpers.
sys.setrecursionlimit(2000)

class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree that acts as a
    dictionary-like set for integers.

    A splay tree is a self-adjusting binary search tree with the additional
    property that recently accessed elements are quick to access again.
    It performs basic operations such as insertion, look-up, and removal
    in O(log n) amortized time.
    """

    class _Node:
        """A private node class for the SplayTree."""
        def __init__(self, key: int):
            self.key: int = key
            self.parent: Optional['SplayTree._Node'] = None
            self.left: Optional['SplayTree._Node'] = None
            self.right: Optional['SplayTree._Node'] = None

    def __init__(self):
        """Initializes an empty SplayTree."""
        self.root: Optional[SplayTree._Node] = None

    def _left_rotate(self, x: _Node):
        """Performs a left rotation on the subtree rooted at x."""
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

    def _right_rotate(self, x: _Node):
        """Performs a right rotation on the subtree rooted at x."""
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

    def _splay(self, x: _Node):
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
            elif x == p.left and p == g.left:  # Zig-zig case (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-zig case (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-zag case (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-zag case (right-left): x == p.left and p == g.right
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree.

        This method performs the splaying operation on the accessed node
        (or its parent if the node is not found) to move it to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_node = None
        while current:
            last_node = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:  # key == current.key
                self._splay(current)
                return True
        
        # Key not found, splay the last visited node to the root.
        if last_node:
            self._splay(last_node)
        
        return False

    def insert(self, key: int):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted and the new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        # Handle empty tree case
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree on the key to bring the closest node to the root
        self.search(key)

        # After search, the root is the node with the key or the closest one.
        # If the key is already present, search has already splayed it and we're done.
        if self.root.key == key:
            return

        # Create the new node and insert it by splitting the tree
        new_node = self._Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if new_node.left:
                new_node.left.parent = new_node
            self.root.left = None
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if new_node.right:
                new_node.right.parent = new_node
            self.root.right = None
        
        self.root.parent = new_node
        self.root = new_node

    def delete(self, key: int):
        """
        Deletes a key from the tree.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the tree on the key. If found, it will be at the root.
        self.search(key)

        # If the key is not at the root after splaying, it wasn't in the tree.
        if self.root.key != key:
            return

        # The node to delete is now at the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree to be the new root.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        elif not right_subtree:
            # Promote the left subtree to be the new root.
            self.root = left_subtree
            if self.root:
                self.root.parent = None
        else:
            # Both subtrees exist. Join them.
            # Disconnect the left subtree to work on it independently.
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max element to the root of the (now separate) left subtree.
            # We temporarily set self.root to perform the splay within this subtree.
            self.root = left_subtree
            self._splay(max_node)
            
            # self.root is now the max_node of the original left subtree.
            # By property, it has no right child. Attach the original right subtree here.
            self.root.right = right_subtree
            right_subtree.parent = self.root