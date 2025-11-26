class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Utility functions
    def _rotate_left(self, x):
        y = x.right
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            p = x.parent
            gp = p.parent
            if gp is None:
                # Zig
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if x == p.left and p == gp.left:
                    # Zig-zig
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif x == p.right and p == gp.right:
                    # Zig-zig
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif x == p.right and p == gp.left:
                    # Zig-zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif x == p.left and p == gp.right:
                    # Zig-zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

    def search(self, key):
        """
        Search for key. If found, splay the node to root.
        If not found, splay the last accessed node (its parent) to root.
        Returns True if key found, False otherwise.
        """
        x = self.root
        last = None
        while x:
            last = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self._splay(x)
                return True
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        """
        Insert key into the tree if it does not exist.
        After insertion, splay the new node to the root.
        """
        if self.root is None:
            self.root = self.Node(key)
            return
        x = self.root
        parent = None
        while x:
            parent = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                # Key already in tree, splay it
                self._splay(x)
                return
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def delete(self, key):
        """
        Delete key from the tree if it exists.
        After deletion, the root will be the splayed parent of the deleted node (if any).
        """
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found, nothing to delete
        node = self.root  # After search(key), node to delete (if it exists) is at root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find max in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            if max_left.parent != node:
                self._replace(max_left, max_left.left)
                max_left.left = node.left
                if max_left.left:
                    max_left.left.parent = max_left
            self._replace(node, max_left)
            max_left.right = node.right
            if max_left.right:
                max_left.right.parent = max_left
        # No need to splay after deletion; splaying is done in search

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        else:
            if u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: for debugging
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res