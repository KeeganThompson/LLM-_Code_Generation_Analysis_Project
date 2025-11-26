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
                return
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

    def _find(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key == x.key:
                return x
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        return last

    def delete(self, key):
        node = self._find(key)
        if not node or node.key != key:
            if node:
                self._splay(node)
            return  # Key not found, do nothing
        self._splay(node)
        # Now node is root
        if not node.left:
            self._replace_root(node.right)
        elif not node.right:
            self._replace_root(node.left)
        else:
            # Find max in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            if max_left.parent != node:
                self._splay(max_left)
                max_left.right = node.right
                if node.right:
                    node.right.parent = max_left
                self._replace_root(max_left)
            else:
                max_left.right = node.right
                if node.right:
                    node.right.parent = max_left
                self._replace_root(max_left)
        del node  # For clarity, not strictly needed in Python

    def _replace_root(self, node):
        if node:
            node.parent = None
        self.root = node

    # Optional: For debugging or in-order traversal
    def inorder(self):
        res = []
        def dfs(node):
            if node:
                dfs(node.left)
                res.append(node.key)
                dfs(node.right)
        dfs(self.root)
        return res