class SplayTree:
    class Node:
        __slots__ = ['key', 'left', 'right', 'parent']
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

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
                    # Zig-Zig
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif x == p.right and p == gp.right:
                    # Zig-Zig
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif x == p.right and p == gp.left:
                    # Zig-Zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif x == p.left and p == gp.right:
                    # Zig-Zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

    def search(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key == x.key:
                self._splay(x)
                return True
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        x = self.root
        while True:
            if key == x.key:
                self._splay(x)
                return
            elif key < x.key:
                if x.left:
                    x = x.left
                else:
                    x.left = self.Node(key, x)
                    self._splay(x.left)
                    return
            else:
                if x.right:
                    x = x.right
                else:
                    x.right = self.Node(key, x)
                    self._splay(x.right)
                    return

    def _subtree_minimum(self, x):
        while x.left:
            x = x.left
        return x

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

    def delete(self, key):
        if self.root is None:
            return
        x = self.root
        while x:
            if key == x.key:
                self._splay(x)
                break
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        else:
            # Not found, splay last accessed node (for locality)
            if x is None and self.root:
                # already splayed in search
                pass
            return
        # Now x is root and has key == key
        if x.left is None:
            self._replace(x, x.right)
        elif x.right is None:
            self._replace(x, x.left)
        else:
            # Both children exist
            y = self._subtree_minimum(x.right)
            if y.parent != x:
                self._replace(y, y.right)
                y.right = x.right
                y.right.parent = y
            self._replace(x, y)
            y.left = x.left
            y.left.parent = y
        # x is now removed

    # For debugging and visualization
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)

    def to_list(self):
        res = []
        self._inorder(self.root, res)
        return res

    # For set-like membership
    def __contains__(self, key):
        return self.search(key)

    # For set-like insertion
    def add(self, key):
        self.insert(key)

    # For set-like deletion
    def discard(self, key):
        self.delete(key)