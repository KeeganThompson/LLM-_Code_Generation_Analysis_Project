import sys

class SplayTree:
    """
    A self-contained Splay Tree class implementing a dictionary-like set for integers.
    It supports insert, delete, and search operations. The search operation
    (and consequently insert and delete which use it) splays the accessed node
    or its parent to the root.
    """

    class _Node:
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
        Splays the node x to the root of the tree.
        This operation moves the node x to the root through a series of rotations.
        """
        while x.parent:
            p = x.parent
            g = p.parent  # Grandparent

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
        
        Performs the splaying operation on the accessed node if found,
        or on its parent if the node is not found.
        
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
            if key == current.key:
                self._splay(current)
                return True
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        
        # Key not found, splay the last visited node (parent of the null spot)
        if last_visited:
            self._splay(last_visited)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.
        
        If the key already exists, it splays the existing node.
        If the key is new, it inserts the node and then splays it to the root.
        
        Args:
            key: The integer key to insert.
        """
        # Standard BST insert part
        parent = None
        current = self.root
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

        new_node = self._Node(key)
        new_node.parent = parent

        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        # Splay the newly inserted node
        self._splay(new_node)

    def delete(self, key):
        """
        Deletes a key from the tree.
        
        It first searches for the key, which splays the node (or a neighbor)
        to the root. If the key is found at the root, it is removed, and
        the remaining subtrees are joined.
        
        Args:
            key: The integer key to delete.
        """
        # Search for the key. This will splay the node to the root if it exists,
        # or a neighbor if it doesn't.
        if not self.search(key):
            return  # Key not in tree

        # After search, if the key was found, it must be the root.
        # If the root's key is not what we want to delete, it means the key
        # was not in the tree and search() splayed a neighbor.
        if self.root.key != key:
            return

        # At this point, the node to delete is the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # If there's no left subtree, the right subtree becomes the new tree.
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # Find the maximum element in the left subtree.
            max_in_left = left_subtree
            while max_in_left.right:
                max_in_left = max_in_left.right
            
            # Splay this maximum element to the root of the left subtree.
            # Temporarily make the left subtree its own tree to perform the splay.
            left_subtree.parent = None
            # The next two lines are a trick to reuse the _splay method
            # on the left subtree.
            temp_root = self.root 
            self.root = left_subtree
            self._splay(max_in_left) # Now, self.root is max_in_left
            
            # The new root of the combined tree is max_in_left.
            # Its right child (which is now None) becomes the original right subtree.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root
            
            # Restore parent pointers correctly (not strictly needed with the trick,
            # but good practice if temp_root was to be reused).
            temp_root = None