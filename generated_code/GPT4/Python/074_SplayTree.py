class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Right rotation
    def _rotate_right(self, x):
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

    # Left rotation
    def _rotate_left(self, x):
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

    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig rotation
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-zig rotation
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-zig rotation
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-zag rotation
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)
            else:
                # Zig-zag rotation
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

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
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
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

    def _subtree_maximum(self, node):
        while node.right:
            node = node.right
        return node

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
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        if not node:
            # Splay the last accessed node (closest parent)
            return
        self._splay(node)
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            max_left = self._subtree_maximum(node.left)
            self._splay(max_left)
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self.root = max_left
            max_left.parent = None

    # For debugging: print in-order
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)

    def to_list(self):
        res = []
        self._inorder(self.root, res)
        return res