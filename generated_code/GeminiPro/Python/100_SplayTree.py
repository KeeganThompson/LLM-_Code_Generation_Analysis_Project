import sys

class SplayTree:
    """
    A complete, self-contained Python class that implements a dictionary-like
    set for integers using a Splay Tree.

    A splay tree is a self-adjusting binary search tree with the additional
    property that recently accessed elements are quick to access again. All
    normal operations on a binary search tree are combined with one basic
    operation, called splaying. Splaying the tree for a certain element
    rearranges the tree so that the element is placed at the root.
    """

    class _Node:
        """A private class representing a node in the splay tree."""
        def __init__(self, key):
            self.key = key
            self.parent = None
            self.left = None
            self.right = None

    def __init__(self):
        """Initializes an empty SplayTree."""
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
        Performs the splay operation on node x, moving it to the root.
        This operation consists of a sequence of rotations (Zig, Zig-Zig, Zig-Zag)
        until x is the root of the tree.
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
            else:  # Zig-Zag case (x is left child of p, p is right child of g)
                self._right_rotate(p)
                self._left_rotate(g)

    def search(self, key):
        """
        Searches for a key in the tree and performs the splaying operation.

        If the key is found, the corresponding node is splayed to the root.
        If the key is not found, the last accessed node before the search
        terminated (i.e., the parent of the would-be key) is splayed to the root.

        Args:
            key: The integer key to search for.

        Returns:
            True if the key is in the tree, False otherwise.
        """
        node = self.root
        last_node = None
        while node:
            last_node = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return True

        # Key not found, splay the last accessed node
        if last_node:
            self._splay(last_node)
        return False

    def insert(self, key):
        """
        Inserts a key into the tree.

        If the key already exists, the existing node is splayed to the root.
        If the key is new, it is inserted as in a standard BST, and then the
        new node is splayed to the root.

        Args:
            key: The integer key to insert.
        """
        parent = None
        current = self.root
        while current:
            parent = current
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                # Key already exists, splay it and return
                self._splay(current)
                return

        # Insert the new node
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

        First, the tree is searched for the key. This splays the node containing
        the key (or a nearby node) to the root. If the key is found at the root,
        it is removed, and its two subtrees are joined.

        Args:
            key: The integer key to delete.
        """
        # Search for the key. This splays the node to the root if found.
        if not self.search(key):
            # Key is not in the tree. search() has already splayed the
            # last accessed node, so we can just return.
            return

        # At this point, the node to be deleted is guaranteed to be the root.
        left_subtree = self.root.left
        right_subtree = self.root.right

        if not left_subtree:
            # Promote the right subtree to be the new root
            self.root = right_subtree
            if right_subtree:
                right_subtree.parent = None
        else:
            # The left subtree becomes the main tree. We need to find the
            # maximum element in the left subtree, splay it to the top of
            # the left subtree, and then attach the right subtree.
            
            # 1. Disconnect the left subtree from the old root
            left_subtree.parent = None
            
            # 2. Find the maximum node in the left subtree
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            
            # 3. Splay this maximum node to the top of its subtree.
            #    We temporarily set the root to the left subtree's root to
            #    use the existing _splay logic.
            self.root = left_subtree
            self._splay(max_node)
            
            # 4. After splaying, max_node is the new root. Its right child
            #    is guaranteed to be None. We attach the original right subtree here.
            self.root.right = right_subtree
            if right_subtree:
                right_subtree.parent = self.root