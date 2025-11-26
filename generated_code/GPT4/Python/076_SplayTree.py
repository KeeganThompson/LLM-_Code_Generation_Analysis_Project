class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Rotate node x up
    def _rotate(self, x):
        p = x.parent
        if not p:
            return
        g = p.parent
        if p.left == x:
            b = x.right
            x.right = p
            p.left = b
            if b:
                b.parent = p
        else:
            b = x.left
            x.left = p
            p.right = b
            if b:
                b.parent = p
        x.parent = g
        p.parent = x
        if g:
            if g.left == p:
                g.left = x
            else:
                g.right = x
        else:
            self.root = x

    # Splay node x to root, or x's parent if x is not found (optional)
    def _splay(self, x):
        if not x:
            return
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                # Zig
                self._rotate(x)
            elif (g.left == p and p.left == x) or (g.right == p and p.right == x):
                # Zig-Zig
                self._rotate(p)
                self._rotate(x)
            else:
                # Zig-Zag
                self._rotate(x)
                self._rotate(x)

    # Search for key, splay the found node or last accessed parent to root
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
                # Found, splay x
                self._splay(x)
                return True
        # Not found, splay last accessed node (prev)
        if prev:
            self._splay(prev)
        return False

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        x = self.root
        while True:
            if key < x.key:
                if x.left:
                    x = x.left
                else:
                    x.left = self.Node(key, parent=x)
                    self._splay(x.left)
                    break
            elif key > x.key:
                if x.right:
                    x = x.right
                else:
                    x.right = self.Node(key, parent=x)
                    self._splay(x.right)
                    break
            else:
                # Key already present; splay x
                self._splay(x)
                break

    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found
        # Now root.key == key
        x = self.root
        if not x.left:
            self._replace_root(x.right)
        elif not x.right:
            self._replace_root(x.left)
        else:
            # Find max in left subtree
            y = x.left
            while y.right:
                y = y.right
            # Splay y to root of left subtree
            self._splay(y)
            # y is now root.left, and has no right child
            y.right = x.right
            if x.right:
                x.right.parent = y
            self._replace_root(y)

    def _replace_root(self, node):
        self.root = node
        if node:
            node.parent = None

    # For debugging: inorder traversal as a list
    def inorder(self):
        def _inorder(x):
            if not x:
                return []
            return _inorder(x.left) + [x.key] + _inorder(x.right)
        return _inorder(self.root)