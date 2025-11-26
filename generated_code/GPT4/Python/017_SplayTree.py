class SplayTree:
    class Node:
        __slots__ = 'key', 'left', 'right', 'parent'
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None

    def _left_rotate(self, x):
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        if y:
            y.left = x
        x.parent = y

    def _right_rotate(self, x):
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
        if not x:
            return
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:
                # Zig
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            else:
                if x == p.left and p == gp.left:
                    # Zig-Zig
                    self._right_rotate(gp)
                    self._right_rotate(p)
                elif x == p.right and p == gp.right:
                    # Zig-Zig
                    self._left_rotate(gp)
                    self._left_rotate(p)
                elif x == p.right and p == gp.left:
                    # Zig-Zag
                    self._left_rotate(p)
                    self._right_rotate(gp)
                elif x == p.left and p == gp.right:
                    # Zig-Zag
                    self._right_rotate(p)
                    self._left_rotate(gp)

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
        if not self.root:
            self.root = self.Node(key)
            return
        x = self.root
        p = None
        while x:
            p = x
            if key == x.key:
                self._splay(x)
                return
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        node = self.Node(key)
        node.parent = p
        if key < p.key:
            p.left = node
        else:
            p.right = node
        self._splay(node)

    def _subtree_minimum(self, x):
        while x.left:
            x = x.left
        return x

    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found, nothing to delete
        node = self.root
        # At this point, node.key == key and node is root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Find minimum of right subtree
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
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent