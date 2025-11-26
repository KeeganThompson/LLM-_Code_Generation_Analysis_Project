class SplayTree:
    class Node:
        __slots__ = ('key', 'left', 'right', 'parent')
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
        node = self.root
        last = None
        while node:
            last = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return  # Already present, do nothing
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self, key):
        if self.root is None:
            return
        # Splay key to root (or last accessed node if not found)
        self.search(key)
        if self.root and self.root.key == key:
            if self.root.left is None:
                self.root = self.root.right
                if self.root:
                    self.root.parent = None
            elif self.root.right is None:
                self.root = self.root.left
                if self.root:
                    self.root.parent = None
            else:
                # Find minimum in right subtree
                min_right = self._subtree_minimum(self.root.right)
                if min_right.parent != self.root:
                    self._splay(min_right)
                    min_right.left = self.root.left
                    if min_right.left:
                        min_right.left.parent = min_right
                else:
                    min_right.left = self.root.left
                    if min_right.left:
                        min_right.left.parent = min_right
                self.root = min_right
                self.root.parent = None

    # Optional: for testing purposes
    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        def _recurse(node):
            if node is None:
                return []
            return _recurse(node.left) + [node.key] + _recurse(node.right)
        return str(_recurse(self.root))