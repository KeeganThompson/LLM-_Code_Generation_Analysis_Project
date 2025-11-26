class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

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
        elif x == x.parent.left:
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
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig
                if x.parent.left == x:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-Zig
                self._right_rotate(x.parent.parent)
                self._right_rotate(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-Zig
                self._left_rotate(x.parent.parent)
                self._left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-Zag
                self._right_rotate(x.parent)
                self._left_rotate(x.parent)
            else:
                # Zig-Zag
                self._left_rotate(x.parent)
                self._right_rotate(x.parent)

    def insert(self, key):
        if not self.root:
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
                # Key already exists; splay it to root
                self._splay(node)
                return
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

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
        # Not found: splay last accessed node (parent of where key would be)
        if last:
            self._splay(last)
        return False

    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return
        # Now, self.root.key == key
        node = self.root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Find min of right subtree
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            if min_node.parent != node:
                self._replace(min_node, min_node.right)
                min_node.right = node.right
                if min_node.right:
                    min_node.right.parent = min_node
            self._replace(node, min_node)
            min_node.left = node.left
            if min_node.left:
                min_node.left.parent = min_node

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: in-order traversal for debugging
    def inorder(self):
        def _inorder(node):
            return _inorder(node.left) + [node.key] + _inorder(node.right) if node else []
        return _inorder(self.root)