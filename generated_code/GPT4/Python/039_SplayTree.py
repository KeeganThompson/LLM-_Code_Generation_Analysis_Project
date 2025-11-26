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
        while x.parent:
            if x.parent.parent is None:
                # Zig step
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                if x == x.parent.left and x.parent == x.parent.parent.left:
                    # Zig-zig step
                    self._rotate_right(x.parent.parent)
                    self._rotate_right(x.parent)
                elif x == x.parent.right and x.parent == x.parent.parent.right:
                    # Zig-zig step
                    self._rotate_left(x.parent.parent)
                    self._rotate_left(x.parent)
                elif x == x.parent.right and x.parent == x.parent.parent.left:
                    # Zig-zag step
                    self._rotate_left(x.parent)
                    self._rotate_right(x.parent)
                elif x == x.parent.left and x.parent == x.parent.parent.right:
                    # Zig-zag step
                    self._rotate_right(x.parent)
                    self._rotate_left(x.parent)

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        node = self.root
        while True:
            if key == node.key:
                self._splay(node)
                return  # key already in tree, do nothing
            elif key < node.key:
                if node.left is None:
                    node.left = self.Node(key, parent=node)
                    self._splay(node.left)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = self.Node(key, parent=node)
                    self._splay(node.right)
                    return
                node = node.right

    def _subtree_max(self, node):
        while node.right:
            node = node.right
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
        parent = None
        while node:
            if key == node.key:
                self._splay(node)
                break
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        else:
            # key not found, splay parent if exists
            if parent:
                self._splay(parent)
            return  # Key not in tree, do nothing

        # Now node is at root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find max in left subtree
            max_left = self._subtree_max(node.left)
            if max_left.parent != node:
                self._replace(max_left, max_left.left)
                max_left.left = node.left
                max_left.left.parent = max_left
            self._replace(node, max_left)
            max_left.right = node.right
            max_left.right.parent = max_left
            self._splay(max_left)

    def search(self, key):
        node = self.root
        parent = None
        while node:
            if key == node.key:
                self._splay(node)
                return True
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        # Not found: splay the last accessed parent
        if parent:
            self._splay(parent)
        return False

    # Optional: for debugging/testing
    def inorder(self):
        def _inorder(node):
            if node:
                yield from _inorder(node.left)
                yield node.key
                yield from _inorder(node.right)
        return list(_inorder(self.root))