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
        if y is None:
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
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
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
            else:
                # x == x.parent.left and x.parent == x.parent.parent.right
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        x = self.root
        p = None
        while x:
            p = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self._splay(x)
                return  # Key already present, no duplicates in set
        new_node = self.Node(key, parent=p)
        if key < p.key:
            p.left = new_node
        else:
            p.right = new_node
        self._splay(new_node)

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

    def delete(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                break
        if not node:
            # Key not found, splay closest parent
            parent = self._find_parent_for_key(key)
            if parent:
                self._splay(parent)
            return

        self._splay(node)
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
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
        # node is now removed

    def _find_parent_for_key(self, key):
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return parent
        return parent

    def search(self, key):
        x = self.root
        prev = None
        while x:
            prev = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self._splay(x)
                return True
        if prev:
            self._splay(prev)
        return False

    # Optional: iterator and __contains__ for set-like usability
    def __contains__(self, key):
        return self.search(key)

    def __iter__(self):
        stack = []
        node = self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key
            node = node.right