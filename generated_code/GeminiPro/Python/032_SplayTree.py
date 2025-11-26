class SplayTree:
    """
    An implementation of a Splay Tree, a self-balancing binary search tree.
    This class provides a dictionary-like set for storing unique integer keys.
    The key feature is that recently accessed elements are moved to the root
    of the tree, making subsequent accesses to them faster.
    """

    class _Node:
        """A private inner class to represent a node in the Splay Tree."""
        def __init__(self, key: int):
            self.key = key
            self.parent: 'SplayTree._Node' | None = None
            self.left: 'SplayTree._Node' | None = None
            self.right: 'SplayTree._Node' | None = None

    def __init__(self):
        """Initializes an empty Splay Tree."""
        self.root: SplayTree._Node | None = None

    def _left_rotate(self, x: _Node):
        """Performs a left rotation on the subtree rooted at node x."""
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        
        y.parent = x.parent
        if not x.parent:
            # The caller (_splay) is responsible for setting the tree's root.
            pass
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        
        y.left = x
        x.parent = y

    def _right_rotate(self, x: _Node):
        """Performs a right rotation on the subtree rooted at node x."""
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        
        y.parent = x.parent
        if not x.parent:
            # The caller (_splay) is responsible for setting the tree's root.
            pass
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
            
        y.right = x
        x.parent = y

    def _splay(self, x: _Node):
        """
        Performs the splaying operation on node x, moving it to become the
        root of the subtree it belongs to.
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
            else:  # Zig-zag case (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key: int) -> bool:
        """
        Searches for a key in the tree.
        
        Performs the splaying operation on the accessed node if found,
        or on its parent if not found. This moves the relevant node to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is found, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key == node.key:
                self._splay(node)
                self.root = node
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # Key not found, splay the last visited node (parent)
        if last_node:
            self._splay(last_node)
            self.root = last_node
        
        return False

    def insert(self, key: int) -> None:
        """
        Inserts a key into the tree.
        
        If the key already exists, it is splayed to the root.
        If the key is new, it is inserted and then splayed to the root.

        Args:
            key: The integer key to insert.
        """
        # Case 1: Tree is empty
        if not self.root:
            self.root = self._Node(key)
            return

        # Splay the tree on the key. This brings the closest node to the root.
        self.search(key)
        
        # After search, self.root is the node with the key or the closest node.
        if self.root.key == key:
            return  # Key already exists, search() already splayed it.

        # The key is not in the tree, so we insert a new node by splitting the tree.
        new_node = self._Node(key)
        
        if key < self.root.key:
            # New node becomes the root.
            # Old root becomes the right child of the new node.
            # Old root's left subtree becomes the left child of the new node.
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
            self.root.parent = new_node
        else:  # key > self.root.key
            # New node becomes the root.
            # Old root becomes the left child of the new node.
            # Old root's right subtree becomes the right child of the new node.
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None
            self.root.parent = new_node
        
        self.root = new_node

    def delete(self, key: int) -> None:
        """
        Deletes a key from the tree.
        
        If the key is found, it is splayed to the root and then removed.
        The tree is then re-joined. If not found, the tree is splayed
        on the last accessed node.

        Args:
            key: The integer key to delete.
        """
        if not self.root:
            return

        # Splay the tree on the key. If not found, search() splays the parent.
        if not self.search(key):
            return # Key not found, nothing to delete.

        # Now, the node to be deleted is guaranteed to be the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if self.root:
                self.root.parent = None
        else:
            # Disconnect the left subtree to work on it.
            left_subtree.parent = None
            
            # Find the maximum element in the left subtree.
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # Splay this maximum element to the root of the (disconnected) left subtree.
            # After this, max_node is the root of this subtree and has no right child.
            self._splay(max_node)
            
            # Join the original right subtree to the new root of the left subtree.
            max_node.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_node
            
            self.root = max_node