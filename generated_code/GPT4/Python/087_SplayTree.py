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
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x.parent.left == x:
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
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            p = x.parent
            gp = p.parent
            if gp is None:
                # Zig
                if p.left == x:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if gp.left == p and p.left == x:
                    # Zig-Zig
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif gp.right == p and p.right == x:
                    # Zig-Zig
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif gp.left == p and p.right == x:
                    # Zig-Zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif gp.right == p and p.left == x:
                    # Zig-Zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        curr = self.root
        parent = None
        while curr:
            parent = curr
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                # Already in set: splay and return
                self._splay(curr)
                return
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def search(self, key):
        curr = self.root
        prev = None
        while curr:
            if key < curr.key:
                prev = curr
                curr = curr.left
            elif key > curr.key:
                prev = curr
                curr = curr.right
            else:
                self._splay(curr)
                return True
        if prev:
            self._splay(prev)
        return False

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

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
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                break
        else:
            # Not found; splay the last accessed node if tree is not empty
            return

        # Now node is at root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            min_right = self._subtree_minimum(node.right)
            if min_right.parent != node:
                self._replace(min_right, min_right.right)
                min_right.right = node.right
                min_right.right.parent = min_right
            self._replace(node, min_right)
            min_right.left = node.left
            min_right.left.parent = min_right

    # Optional: for debugging and testing
    def inorder(self):
        def _inorder(node):
            if node:
                yield from _inorder(node.left)
                yield node.key
                yield from _inorder(node.right)
        return list(_inorder(self.root))