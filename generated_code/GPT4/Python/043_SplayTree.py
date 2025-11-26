class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Right rotate x
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

    # Left rotate x
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

    # Splay x to the root
    def _splay(self, x):
        while x.parent:
            if x.parent.parent is None:
                # Zig
                if x.parent.left == x:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            else:
                p = x.parent
                g = p.parent
                if p.left == x and g.left == p:
                    # Zig-zig
                    self._right_rotate(g)
                    self._right_rotate(p)
                elif p.right == x and g.right == p:
                    # Zig-zig
                    self._left_rotate(g)
                    self._left_rotate(p)
                elif p.left == x and g.right == p:
                    # Zig-zag
                    self._right_rotate(p)
                    self._left_rotate(g)
                elif p.right == x and g.left == p:
                    # Zig-zag
                    self._left_rotate(p)
                    self._right_rotate(g)

    # Search for key, splay found node or last accessed parent
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

    # Insert key if not present
    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        x = self.root
        parent = None
        while x:
            parent = x
            if key == x.key:
                self._splay(x)
                return  # Key already in set, do nothing
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

    # Delete key if present
    def delete(self, key):
        if not self.search(key):
            return  # Key not found
        # Now root is the node to delete
        to_delete = self.root
        if to_delete.left is None:
            self._replace(to_delete, to_delete.right)
        elif to_delete.right is None:
            self._replace(to_delete, to_delete.left)
        else:
            # Find minimum in right subtree
            y = to_delete.right
            while y.left:
                y = y.left
            if y.parent != to_delete:
                self._replace(y, y.right)
                y.right = to_delete.right
                if y.right:
                    y.right.parent = y
            self._replace(to_delete, y)
            y.left = to_delete.left
            if y.left:
                y.left.parent = y

    # Replace subtree u with v
    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Utility: In-order traversal (for debugging, not required)
    def inorder(self):
        res = []
        def dfs(node):
            if node:
                dfs(node.left)
                res.append(node.key)
                dfs(node.right)
        dfs(self.root)
        return res