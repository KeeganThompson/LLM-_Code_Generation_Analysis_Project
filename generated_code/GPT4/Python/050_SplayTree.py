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
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-Zig step (left-left)
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-Zig step (right-right)
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-Zag step (left-right)
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)
            else:
                # Zig-Zag step (right-left)
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return

        curr = self.root
        parent = None
        while curr:
            parent = curr
            if key == curr.key:
                self._splay(curr)
                return
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

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
        parent = None
        while node:
            if key == node.key:
                break
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right

        if node is None:
            # Key not found, splay the last accessed parent
            if parent:
                self._splay(parent)
            return

        self._splay(node)

        # After splaying, node is at root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find max in left subtree
            max_left = self._subtree_maximum(node.left)
            if max_left.parent != node:
                self._replace(max_left, max_left.left)
                max_left.left = node.left
                max_left.left.parent = max_left
            self._replace(node, max_left)
            max_left.right = node.right
            if max_left.right:
                max_left.right.parent = max_left
        # No need to free node: Python GC will handle it

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
        # Not found: splay last accessed node (parent)
        if last:
            self._splay(last)
        return False

    # Optional: for debugging/visualization
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)

    def to_list(self):
        res = []
        self._inorder(self.root, res)
        return res