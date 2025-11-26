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
        if y.left is not None:
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
        if y.right is not None:
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
        while x.parent is not None:
            p = x.parent
            gp = p.parent
            if gp is None:
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if x == p.left and p == gp.left:
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif x == p.right and p == gp.right:
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif x == p.right and p == gp.left:
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif x == p.left and p == gp.right:
                    self._rotate_right(p)
                    self._rotate_left(gp)

    def search(self, key):
        x = self.root
        last = None
        while x is not None:
            last = x
            if key == x.key:
                self._splay(x)
                return True
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        if last is not None:
            self._splay(last)
        return False

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        x = self.root
        parent = None
        while x is not None:
            parent = x
            if key == x.key:
                self._splay(x)
                return
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def _subtree_minimum(self, x):
        while x.left is not None:
            x = x.left
        return x

    def delete(self, key):
        if not self.search(key):
            return
        node = self.root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            min_right = self._subtree_minimum(node.right)
            if min_right.parent != node:
                self._replace(min_right, min_right.right)
                min_right.right = node.right
                if min_right.right:
                    min_right.right.parent = min_right
            self._replace(node, min_right)
            min_right.left = node.left
            if min_right.left:
                min_right.left.parent = min_right

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        else:
            if u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def _inorder(self, node, res):
        if node is not None:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)

    def keys(self):
        res = []
        self._inorder(self.root, res)
        return res