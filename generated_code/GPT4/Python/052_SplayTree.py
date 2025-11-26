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

    # Rotate node x up
    def _rotate(self, x):
        p = x.parent
        if p is None:
            return
        g = p.parent
        if p.left == x:
            # Right rotation
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
            # Left rotation
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p
        p.parent = x
        x.parent = g
        if g:
            if g.left == p:
                g.left = x
            else:
                g.right = x
        else:
            self.root = x

    # Splay x to root
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            p = x.parent
            g = p.parent
            if g is None:
                # Zig
                self._rotate(x)
            elif (g.left == p and p.left == x) or (g.right == p and p.right == x):
                # Zig-zig
                self._rotate(p)
                self._rotate(x)
            else:
                # Zig-zag
                self._rotate(x)
                self._rotate(x)

    def _subtree_min(self, x):
        while x.left:
            x = x.left
        return x

    def _subtree_max(self, x):
        while x.right:
            x = x.right
        return x

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
        # Splay the parent of the last accessed node (if tree is not empty)
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        x = self.root
        p = None
        while x:
            p = x
            if key == x.key:
                self._splay(x)
                return  # Key already exists
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        new_node = self.Node(key, p)
        if key < p.key:
            p.left = new_node
        else:
            p.right = new_node
        self._splay(new_node)

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
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found, nothing to do
        node = self.root
        # Now node.key == key
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find min in right subtree
            y = self._subtree_min(node.right)
            if y.parent != node:
                self._replace(y, y.right)
                y.right = node.right
                y.right.parent = y
            self._replace(node, y)
            y.left = node.left
            y.left.parent = y
        # No need to splay after delete

    # Optional: for debugging
    def inorder(self):
        res = []
        def _in(x):
            if not x:
                return
            _in(x.left)
            res.append(x.key)
            _in(x.right)
        _in(self.root)
        return res