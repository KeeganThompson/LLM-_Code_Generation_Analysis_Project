import typing

class SplayTree:
    """
    A complete, self-contained implementation of a Splay Tree.

    This class provides a dictionary-like set for storing unique integer keys.
    It supports insertion, deletion, and search operations, all of which
    involve a 'splaying' step. Splaying moves the accessed (or newly inserted/deleted)
    node to the root of the tree, which optimizes for temporal locality of reference,
    making frequently accessed elements faster to retrieve.
    """

    class _Node:
        """A node in the splay tree."""
        def __init__(self, key: int):
            self.key: int = key
            self.parent: typing.Optional[SplayTree._Node] = None
            self.left: typing.Optional[SplayTree._Node] = None
            self.right: typing.Optional[SplayTree._Node] = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root: typing.Optional[SplayTree._Node] = None

    def _left_rotate(self, x: _Node):
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

    def _right_rotate(self, x: _Node):
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

    def _splay(self, x: _Node):
        """
        Performs the splaying operation on node x, moving it to the root.
        """
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:  # Zig case
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == g.left:  # Zig-Zig case
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig case
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag case
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag case (x == p.left and p == g.right)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree.

        This method performs the splaying operation on the accessed node if the key
        is found, or on its parent if the key is not found. This moves the
        relevant node to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        if not self.root:
            return False

        last_visited = None
        current = self.root
        while current:
            last_visited = current
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node (the parent of the null spot)
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key: int):
        """
        Inserts a key into the tree.

        If the key already exists, the node with that key is splayed to the root.
        If the key is new, it is inserted as a new node and then splayed to the root.
        """
        if not self.root:
            self.root = self._Node(key)
            return

        current = self.root
        parent = None
        while current:
            parent = current
            if key == current.key:
                # Key already exists, splay the node and finish
                self._splay(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, create and insert the new node
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

        The tree is first splayed on the key. If the key exists, it will be at
        the root. The root is then removed, and its left and right subtrees
        are joined.
        """
        if not self.root:
            return

        # Splay the node with the key (or its last-accessed parent) to the root
        self.search(key)

        # After search, if the key exists, it's at the root.
        # If not, a neighbor is at the root. We must check.
        if self.root.key != key:
            return  # Key was not in the tree

        # The node to delete is now at the root
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # No left child, so the right subtree becomes the new tree
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree to work on it
            left_subtree.parent = None
            
            # Find the maximum node in the left subtree
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Splay this maximum node. It will become the new root of the
            # combined tree. We do this by temporarily treating the left
            # subtree as the main tree.
            self.root = left_subtree
            self._splay(max_in_left)
            
            # After splaying, self.root is the new root (max_in_left).
            # It has no right child, so we can attach the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root