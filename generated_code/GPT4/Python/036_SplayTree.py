class SplayTree:
    class Node:
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
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if x.parent.parent is None:
                # Zig
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
        # Not found, splay last accessed node (parent of null)
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
                return  # Key already in set
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        new_node = self.Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def delete(self, key):
        if not self.root:
            return

        if not self.search(key):
            return  # Key not found

        # Now root.key == key
        node = self.root

        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find min in right subtree
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            if min_node.parent != node:
                self._replace(min_node, min_node.right)
                min_node.right = node.right
                if min_node.right:
                    min_node.right.parent = min_node
            self._replace(node, min_node)
            min_node.left = node.left
            if min_node.left:
                min_node.left.parent = min_node

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: For debug/testing
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res