class SplayTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None

    def _left_rotate(self, x):
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

    def _right_rotate(self, x):
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
                # Zig case
                if x == x.parent.left:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-zig case
                self._right_rotate(x.parent.parent)
                self._right_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-zig case
                self._left_rotate(x.parent.parent)
                self._left_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-zag case
                self._left_rotate(x.parent)
                self._right_rotate(x.parent)
            else:
                # Zig-zag case
                self._right_rotate(x.parent)
                self._left_rotate(x.parent)

    def _subtree_minimum(self, x):
        while x.left:
            x = x.left
        return x

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def insert(self, key):
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
                return  # Key already in set, do nothing
        new_node = self.Node(key)
        new_node.parent = parent
        if not parent:
            self.root = new_node
        elif key < parent.key:
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
        if not self.search(key):  # splay closest node to root
            return  # Key not found
        node = self.root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            y = self._subtree_minimum(node.right)
            if y.parent != node:
                self._replace(y, y.right)
                y.right = node.right
                if y.right:
                    y.right.parent = y
            self._replace(node, y)
            y.left = node.left
            if y.left:
                y.left.parent = y

    # For testing/debugging
    def inorder(self):
        res = []
        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            res.append(node.key)
            _inorder(node.right)
        _inorder(self.root)
        return res