class SplayTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

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
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if x.parent.parent is None:
                # Zig
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if g.left == p and p.left == x:
                    # Zig-Zig (left-left)
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif g.right == p and p.right == x:
                    # Zig-Zig (right-right)
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif g.left == p and p.right == x:
                    # Zig-Zag (left-right)
                    self._rotate_left(p)
                    self._rotate_right(g)
                else:
                    # Zig-Zag (right-left)
                    self._rotate_right(p)
                    self._rotate_left(g)

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
        # Key not found, splay last accessed node (parent)
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return  # Key already present, treat as set
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        new_node = self.Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def delete(self, key):
        if self.root is None:
            return
        if not self.search(key):
            return  # Key not in tree, nothing to do
        node = self.root
        # Now node.key == key
        if node.left is None:
            self._transplant(node, node.right)
        elif node.right is None:
            self._transplant(node, node.left)
        else:
            # Find minimum in right subtree
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            if min_node.parent != node:
                self._transplant(min_node, min_node.right)
                min_node.right = node.right
                if min_node.right:
                    min_node.right.parent = min_node
            self._transplant(node, min_node)
            min_node.left = node.left
            if min_node.left:
                min_node.left.parent = min_node

    def _transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: For debugging and visualization only
    def inorder(self):
        def _inorder(node):
            return _inorder(node.left) + [node.key] + _inorder(node.right) if node else []
        return _inorder(self.root)