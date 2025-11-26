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
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if g.left == p and p.left == x:
                    # Zig-zig step
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif g.right == p and p.right == x:
                    # Zig-zig step
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif g.left == p and p.right == x:
                    # Zig-zag step
                    self._rotate_left(p)
                    self._rotate_right(g)
                elif g.right == p and p.left == x:
                    # Zig-zag step
                    self._rotate_right(p)
                    self._rotate_left(g)

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
                # Key already exists, splay it
                self._splay(node)
                return

        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._splay(new_node)

    def search(self, key):
        node = self.root
        last = None
        while node:
            last = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return True
        if last:
            self._splay(last)
        return False

    def delete(self, key):
        if not self.root:
            return

        if not self.search(key):
            return  # Key not found, nothing to delete

        node = self.root  # After search, node with key (if exists) is at root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find maximum in left subtree
            y = node.left
            while y.right:
                y = y.right
            if y.parent != node:
                self._replace(y, y.left)
                y.left = node.left
                if y.left:
                    y.left.parent = y
            self._replace(node, y)
            y.right = node.right
            if y.right:
                y.right.parent = y

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # For debugging: inorder traversal as a list
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res