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
        if y.left is not None:
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
        if y.right is not None:
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
        while x.parent is not None:
            if x.parent.parent is None:
                # Zig step
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-Zig step
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-Zig step
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-Zag step
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)
            else:
                # Zig-Zag step
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

    def search(self, key):
        node = self.root
        last = None
        while node is not None:
            last = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        # Splay the last accessed node (parent of where key would be)
        if last is not None:
            self._splay(last)
        return False

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node is not None:
            parent = node
            if key == node.key:
                self._splay(node)
                return
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def delete(self, key):
        if not self.search(key):
            return
        # Now self.root.key == key
        root = self.root
        if root.left is None:
            self.root = root.right
            if self.root is not None:
                self.root.parent = None
        elif root.right is None:
            self.root = root.left
            if self.root is not None:
                self.root.parent = None
        else:
            # Find max in left subtree
            left_subtree = root.left
            left_subtree.parent = None
            max_left = left_subtree
            while max_left.right is not None:
                max_left = max_left.right
            self._splay(max_left)
            # Now max_left is root of left_subtree and has no right child
            max_left.right = root.right
            if root.right is not None:
                root.right.parent = max_left
            self.root = max_left
            max_left.parent = None

    # Optional: for debugging and testing
    def inorder(self):
        res = []
        def _inorder(node):
            if node is None:
                return
            _inorder(node.left)
            res.append(node.key)
            _inorder(node.right)
        _inorder(self.root)
        return res