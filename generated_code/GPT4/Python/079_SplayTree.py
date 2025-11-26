class SplayTree:
    class Node:
        __slots__ = 'key', 'left', 'right', 'parent'
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
            p = x.parent
            gp = p.parent
            if not gp:
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

    def insert(self, key):
        if self.root is None:
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

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

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
        node = self.root
        last = None
        while node:
            last = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                break
        if node is None:
            # Key not found; splay last accessed node
            if last:
                self._splay(last)
            return
        self._splay(node)
        # Now node is root
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
        # Node is deleted automatically by garbage collection

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

    # Optional: for testing and debugging
    def __contains__(self, key):
        return self.search(key)

    def __repr__(self):
        nodes = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                nodes.append(str(node.key))
                _inorder(node.right)
        _inorder(self.root)
        return "{" + ", ".join(nodes) + "}"