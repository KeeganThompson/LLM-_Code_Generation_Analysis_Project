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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig step
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-zig step
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-zig step
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-zag step
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
            else:
                # Zig-zag step
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return  # Key already exists; do nothing
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def _subtree_max(self, node):
        while node.right:
            node = node.right
        return node

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def delete(self, key):
        node = self.root
        parent = None
        while node:
            if key < node.key:
                parent = node
                node = node.left
            elif key > node.key:
                parent = node
                node = node.right
            else:
                break
        if not node:
            # Key not found; splay last accessed parent if any
            if parent:
                self._splay(parent)
            return

        self._splay(node)
        # Now node is root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Both children exist
            min_right = node.right
            while min_right.left:
                min_right = min_right.left
            if min_right.parent != node:
                self._replace(min_right, min_right.right)
                min_right.right = node.right
                if min_right.right:
                    min_right.right.parent = min_right
            self._replace(node, min_right)
            min_right.left = node.left
            if min_right.left:
                min_right.left.parent = min_right

    def search(self, key):
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return True
        if parent:
            self._splay(parent)
        return False

    # For debugging / testing
    def inorder(self):
        res = []
        def _inorder(n):
            if not n:
                return
            _inorder(n.left)
            res.append(n.key)
            _inorder(n.right)
        _inorder(self.root)
        return res