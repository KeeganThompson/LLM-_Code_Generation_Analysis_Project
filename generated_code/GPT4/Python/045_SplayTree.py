class SplayTree:
    class Node:
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
        while x.parent:
            if x.parent.parent is None:
                # Zig step
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-Zig step
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-Zig step
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-Zag step
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
            else:
                # Zig-Zag step
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)

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
        parent = None
        while x:
            parent = x
            if key == x.key:
                self._splay(x)
                return  # Key already exists, do nothing
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
        if not self.root:
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
            # Key not found; splay last accessed node (parent of NULL)
            return
        # Now x is at root and x.key == key
        if x.left is None:
            self._replace(x, x.right)
        elif x.right is None:
            self._replace(x, x.left)
        else:
            # Both children present
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

    # Optional: For debugging/visualization
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)

    def to_list(self):
        res = []
        self._inorder(self.root, res)
        return res