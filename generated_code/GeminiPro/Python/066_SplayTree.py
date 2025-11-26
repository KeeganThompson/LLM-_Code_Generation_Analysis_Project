class SplayTree:
    """
    A complete, self-contained Splay Tree implementation that supports integer keys
    and provides a dictionary-like set interface.

    The main characteristic of a splay tree is that recently accessed elements
    are quick to access again. It achieves this by moving any accessed node
    (for search, insertion, or deletion) to the root of the tree through a
    series of rotations, an operation called "splaying".
    """

    class Node:
        """A node in the splay tree."""
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
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
            elif x == p.left and p == g.left:  # Zig-Zig case (left-left)
                self._right_rotate(g)
                self._right_rotate(p)
            elif x == p.right and p == g.right:  # Zig-Zig case (right-right)
                self._left_rotate(g)
                self._left_rotate(p)
            elif x == p.right and p == g.left:  # Zig-Zag case (left-right)
                self._left_rotate(p)
                self._right_rotate(g)
            else:  # Zig-Zag case (right-left)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key. If found, splays the node to the root and returns True.
        If not found, splays the last accessed node to the root and returns False.
        """
        node = self.root
        last_visited = None
        while node:
            last_visited = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        
        # If key not found, splay the last visited node
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key. If the key already exists, the existing node is splayed.
        Otherwise, the new node is inserted and splayed to the root.
        """
        # Find position to insert or the existing node
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

        # Create and link the new node
        new_node = self.Node(key)
        new_node.parent = parent
        
        if not parent:  # Tree was empty
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
            
        # Splay the new node to the root
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key. If the key exists, it's removed, and the tree is
        re-formed. If not, the last accessed node from the search is splayed.
        """
        # Search for the key. This splays the found node (or its would-be parent)
        # to the root.
        if not self.search(key):
            # Key not in the tree, nothing to delete.
            # search() has already splayed the last accessed node.
            return

        # At this point, self.root.key must be equal to key because search(key)
        # returned True. The node to delete is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        # Disconnect subtrees from the root
        if left_subtree:
            left_subtree.parent = None
        if right_subtree:
            right_subtree.parent = None

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
        else:
            # Find the maximum element in the left subtree. This element
            # will become the new root of the combined tree.
            new_root = left_subtree
            while new_root.right:
                new_root = new_root.right
            
            # Splay this maximum element to the root of the left subtree.
            # We can do this by temporarily setting the root of our splay operations
            # to be the left subtree.
            self.root = left_subtree
            self._splay(new_root) # After this, self.root is new_root
            
            # The new root (which was the max of the left subtree) is guaranteed
            # to have no right child. We attach the original right subtree here.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root