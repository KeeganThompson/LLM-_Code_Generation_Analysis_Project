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

    # Splay operation
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
            elif x == p.left and p == gp.left:
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
            else:
                # x == p.left and p == gp.right
                self._rotate_right(p)
                self._rotate_left(gp)

    # Search method with splaying
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

    # Insert method
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
                return  # Duplicate, do nothing
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

    # Delete method
    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found
        node = self.root  # After search, key is at root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Find maximum in left subtree
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
        # Remove all references from deleted node
        node.left = node.right = node.parent = None

    # Helper to replace a node with another
    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        else:
            if u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
        if v:
            v.parent = u.parent

    # For debugging: Inorder traversal
    def inorder(self):
        res = []
        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            res.append(node.key)
            _inorder(node.right)
        _inorder(self.root)
        return res