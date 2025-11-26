class SplayTree:
    class Node:
        __slots__ = "key", "left", "right", "parent"
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Right rotation at node x
    def _right_rotate(self, x):
        y = x.left
        if y is None:
            return
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    # Left rotation at node x
    def _left_rotate(self, x):
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

    # Splay operation: bring x to the root
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            p = x.parent
            gp = p.parent
            if gp is None:
                # Zig step
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            elif x == p.left and p == gp.left:
                # Zig-zig step (left-left)
                self._right_rotate(gp)
                self._right_rotate(p)
            elif x == p.right and p == gp.right:
                # Zig-zig step (right-right)
                self._left_rotate(gp)
                self._left_rotate(p)
            elif x == p.right and p == gp.left:
                # Zig-zag step (left-right)
                self._left_rotate(p)
                self._right_rotate(gp)
            elif x == p.left and p == gp.right:
                # Zig-zag step (right-left)
                self._right_rotate(p)
                self._left_rotate(gp)

    # Find node with given key, or last accessed node
    def _find(self, key):
        node = self.root
        prev = None
        while node:
            prev = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node
        return prev

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
                # Key already exists
                self._splay(node)
                return
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def search(self, key):
        node = self._find(key)
        if node is not None:
            self._splay(node)
        if node is not None and node.key == key:
            return True
        else:
            return False

    def delete(self, key):
        node = self._find(key)
        if node is None or node.key != key:
            if node:
                self._splay(node)
            return  # Key not found
        self._splay(node)
        # Now node is root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find max in left subtree
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
        # The root might now be None, or the replacement
        if self.root and self.root.parent:
            self.root = self.root.parent

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: For debugging
    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        def _inorder(node):
            if not node:
                return []
            return _inorder(node.left) + [node.key] + _inorder(node.right)
        return "{" + ", ".join(map(str, _inorder(self.root))) + "}"