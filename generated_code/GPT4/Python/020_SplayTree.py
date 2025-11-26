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

    # Right rotation
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    # Left rotation
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

    # Splaying operation: bring x to root
    def _splay(self, x):
        if not x:
            return
        while x.parent:
            if not x.parent.parent:
                # Zig case
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if x == p.left and p == g.left:
                    # Zig-zig case (left-left)
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif x == p.right and p == g.right:
                    # Zig-zig case (right-right)
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif x == p.right and p == g.left:
                    # Zig-zag case (left-right)
                    self._rotate_left(p)
                    self._rotate_right(g)
                elif x == p.left and p == g.right:
                    # Zig-zag case (right-left)
                    self._rotate_right(p)
                    self._rotate_left(g)

    # Search and splay
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
        # Not found, splay the last accessed node (parent of None)
        if last:
            self._splay(last)
        return False

    # Insert key
    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return

        x = self.root
        p = None
        while x:
            p = x
            if key == x.key:
                self._splay(x)
                return  # Already present, do nothing
            elif key < x.key:
                x = x.left
            else:
                x = x.right

        new_node = self.Node(key, parent=p)
        if key < p.key:
            p.left = new_node
        else:
            p.right = new_node
        self._splay(new_node)

    # Delete key
    def delete(self, key):
        if not self.root:
            return

        if not self.search(key):
            return  # Key not found

        # Now root is the node to delete
        node = self.root
        if not node.left:
            self.root = node.right
            if self.root:
                self.root.parent = None
        elif not node.right:
            self.root = node.left
            if self.root:
                self.root.parent = None
        else:
            # Find the maximum node in left subtree
            left_sub = node.left
            left_sub.parent = None
            max_left = left_sub
            while max_left.right:
                max_left = max_left.right
            # Splay max_left to root of left subtree
            self._splay(max_left)
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self.root = max_left
            self.root.parent = None

    # (Optional) For debugging: inorder traversal
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res