class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    def _rotate_left(self, x):
        y = x.right
        if not y:
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
        if not y:
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
                # Zig
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-zig
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-zig
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-zag
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
            else:
                # Zig-zag
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
        if not self.root:
            self.root = self.Node(key)
            return
        x = self.root
        parent = None
        while x:
            parent = x
            if key == x.key:
                self._splay(x)
                return  # Already in set
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

    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found
        node = self.root
        # Now node.key == key and node is root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Find max in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            if max_left.parent != node:
                self._replace(max_left, max_left.left)
                max_left.left = node.left
                max_left.left.parent = max_left
            self._replace(node, max_left)
            max_left.right = node.right
            if max_left.right:
                max_left.right.parent = max_left

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: for debugging
    def in_order(self):
        res = []
        def inorder(node):
            if not node:
                return
            inorder(node.left)
            res.append(node.key)
            inorder(node.right)
        inorder(self.root)
        return res