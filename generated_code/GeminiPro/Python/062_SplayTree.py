import sys
from typing import Optional, List

# To prevent deep recursion errors on large trees
sys.setrecursionlimit(2000)

class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.
    
    Splay trees are self-balancing binary search trees with the additional property
    that recently accessed elements are quick to access again. It achieves this by
    moving any accessed node to the root of the tree through a series of rotations.
    
    This implementation includes the core methods: insert, delete, and search.
    The search operation performs the splaying.
    """

    class _Node:
        """A node in the Splay Tree."""
        def __init__(self, key: int):
            self.key: int = key
            self.parent: Optional[SplayTree._Node] = None
            self.left: Optional[SplayTree._Node] = None
            self.right: Optional[SplayTree._Node] = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root: Optional[SplayTree._Node] = None

    def _left_rotate(self, x: _Node):
        """Performs a left rotation around node x."""
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
        """Performs a right rotation around node x."""
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

    def _splay(self, node: _Node):
        """
        Performs the splaying operation on a node, moving it to the root.
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
        self.root = node

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree.
        
        Performs the splaying operation on the accessed node if found,
        or on its would-be parent if not found. This moves the relevant
        node to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        current = self.root
        last_visited = None
        while current:
            last_visited = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key found, splay the node
                self._splay(current)
                return True
        
        # Key not found, splay the last visited node (the parent)
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key: int):
        """
        Inserts a key into the tree.
        
        If the key already exists, the node with that key is splayed to the root.
        If the key does not exist, a new node is created, inserted, and then
        splayed to the root.
        
        Args:
            key: The integer key to insert.
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
        
        # Key does not exist, insert new node
        new_node = self._Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        
        # Splay the newly inserted node to the root
        self._splay(new_node)

    def delete(self, key: int):
        """
        Deletes a key from the tree.
        
        The search for the key will cause a splay operation. If the key is
        found, its node is removed from the tree and the remaining subtrees
        are re-joined.
        
        Args:
            key: The integer key to delete.
        """
        # Search for the key. This will splay the node (or its parent) to the root.
        if not self.search(key):
            # Key not in tree. search() already splayed the closest node.
            return

        # After search, if the key was found, it's now the root
        assert self.root and self.root.key == key, "Delete failed: key not at root after search"

        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, the right subtree becomes the new tree
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Disconnect left subtree
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this max node to the root of the left subtree.
            # We can do this by temporarily setting self.root to the left subtree's root.
            self.root = left_subtree
            self._splay(max_node)
            
            # After splaying, max_node is the new root. Re-attach the right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root

    def _in_order_list(self, node: Optional[_Node], result: List[int]):
        """Helper for in-order traversal."""
        if node:
            self._in_order_list(node.left, result)
            result.append(node.key)
            self._in_order_list(node.right, result)

    def __str__(self) -> str:
        """Returns an in-order string representation of the tree."""
        if not self.root:
            return "SplayTree()"
        result: List[int] = []
        self._in_order_list(self.root, result)
        return f"SplayTree({result})"

    def __contains__(self, key: int) -> bool:
        """Allows using the 'in' operator, e.g., 'if key in tree:'."""
        return self.search(key)