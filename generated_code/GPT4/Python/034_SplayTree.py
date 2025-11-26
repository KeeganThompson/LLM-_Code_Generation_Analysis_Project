class SplayTree:
    class Node:
        __slots__ = ['key', 'left', 'right', 'parent']

        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None

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
        elif x == x.parent.left:
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if x.parent.parent is None:
                # Zig step
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-zig step
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-zig step
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-zag step
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)
            else:
                # x == x.parent.left and x.parent == x.parent.parent.right
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

    def search(self, key):
        """
        Search for key.
        Splay the accessed node to root, or the parent if key not found.
        Returns True if found, False otherwise.
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
        Insert key if not present.
        Splays the new or existing node to root.
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
                self._splay(x)
                return  # Key already exists, do nothing
        node = self.Node(key)
        node.parent = parent
        if key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self._splay(node)

    def _subtree_minimum(self, x):
        while x.left:
            x = x.left
        return x

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def delete(self, key):
        """
        Delete key if it exists.
        Splays the parent of the deleted node (or root) to the root.
        """
        x = self.root
        while x:
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self._splay(x)
                # Now x is root
                if x.left is None:
                    self._replace(x, x.right)
                    if self.root:
                        self._splay(self.root)
                elif x.right is None:
                    self._replace(x, x.left)
                    if self.root:
                        self._splay(self.root)
                else:
                    # Find min in right subtree
                    y = self._subtree_minimum(x.right)
                    if y.parent != x:
                        self._replace(y, y.right)
                        y.right = x.right
                        if y.right:
                            y.right.parent = y
                    self._replace(x, y)
                    y.left = x.left
                    if y.left:
                        y.left.parent = y
                    self._splay(y)
                return  # Deleted
        # Key not found; do nothing

    # Optional: For debugging, returns sorted list of keys
    def inorder(self):
        def _inorder(x):
            return _inorder(x.left) + [x.key] + _inorder(x.right) if x else []
        return _inorder(self.root)