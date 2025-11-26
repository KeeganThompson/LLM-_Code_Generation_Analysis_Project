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
        if not y:
            return
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

    def _rotate_right(self, x):
        y = x.left
        if not y:
            return
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
        while x.parent:
            if not x.parent.parent:
                # Zig step
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if x == p.left and p == g.left:
                    # Zig-Zig
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif x == p.right and p == g.right:
                    # Zig-Zig
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif x == p.right and p == g.left:
                    # Zig-Zag
                    self._rotate_left(p)
                    self._rotate_right(g)
                elif x == p.left and p == g.right:
                    # Zig-Zag
                    self._rotate_right(p)
                    self._rotate_left(g)

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        x = self.root
        parent = None
        while x:
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

    def _find(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key == x.key:
                return x, True
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        return last, False

    def search(self, key):
        node, found = self._find(key)
        if node:
            self._splay(node)
        return found

    def delete(self, key):
        node, found = self._find(key)
        if not found:
            if node:
                self._splay(node)
            return
        self._splay(node)
        # Now node is root
        if not node.left:
            self._replace_root(node.right)
        elif not node.right:
            self._replace_root(node.left)
        else:
            # Find the maximum in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            if max_left.parent != node:
                self._replace_node(max_left, max_left.left)
                max_left.left = node.left
                max_left.left.parent = max_left
            self._replace_root(max_left)
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left

    def _replace_root(self, node):
        if node:
            node.parent = None
        self.root = node

    def _replace_node(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: For debug or test purposes
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res