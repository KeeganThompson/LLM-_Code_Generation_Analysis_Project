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

    # --- Core rotation methods ---
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

    # --- Splaying operation ---
    def _splay(self, x):
        if not x:
            return
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:
                # Zig
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if x == p.left and p == gp.left:
                    # Zig-Zig
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif x == p.right and p == gp.right:
                    # Zig-Zig
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif x == p.right and p == gp.left:
                    # Zig-Zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif x == p.left and p == gp.right:
                    # Zig-Zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

    # --- Search operation (with splay) ---
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

    # --- Insert operation ---
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
                return  # Duplicate; do nothing
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

    # --- Delete operation ---
    def delete(self, key):
        if not self.root:
            return
        x = self.root
        while x:
            if key == x.key:
                self._splay(x)
                break
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        else:
            if x is None:
                # Splay the last accessed node
                self.search(key)
            return  # Key not found

        # Now x is at root, and x.key == key
        if not x.left:
            self._transplant(x, x.right)
        elif not x.right:
            self._transplant(x, x.left)
        else:
            # Find minimum in right subtree
            y = x.right
            while y.left:
                y = y.left
            if y.parent != x:
                self._transplant(y, y.right)
                y.right = x.right
                if y.right:
                    y.right.parent = y
            self._transplant(x, y)
            y.left = x.left
            if y.left:
                y.left.parent = y

    def _transplant(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # --- For debugging: in-order traversal (not part of required API) ---
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)

    def keys(self):
        res = []
        self._inorder(self.root, res)
        return res