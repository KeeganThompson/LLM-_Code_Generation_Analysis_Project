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
        if x is None:
            return
        while x.parent:
            p = x.parent
            gp = p.parent
            if gp is None:
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

    def insert(self, key):
        if self.root is None:
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
                # Key already exists, splay and return
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
        # Not found, splay last accessed node (parent of where it would be)
        if last:
            self._splay(last)
        return False

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self, key):
        if self.root is None:
            return
        found = self.search(key)
        if not found:
            return  # Key not found
        # Now, self.root.key == key
        if self.root.left is None:
            self._replace_root(self.root.right)
        elif self.root.right is None:
            self._replace_root(self.root.left)
        else:
            # Both children exist
            right_subtree = self.root.right
            left_subtree = self.root.left
            left_subtree.parent = None
            # Find max in left subtree, splay it
            max_left = left_subtree
            while max_left.right:
                max_left = max_left.right
            self._splay_node_in_subtree(max_left, left_subtree)
            # Now, max_left is root of left_subtree and has no right child
            max_left.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_left
            self.root = max_left
            max_left.parent = None

    def _replace_root(self, node):
        self.root = node
        if node:
            node.parent = None

    def _splay_node_in_subtree(self, node, subtree_root):
        # Splay 'node' to be root of 'subtree_root'
        while node.parent:
            p = node.parent
            gp = p.parent
            if gp is None or gp == subtree_root.parent:
                # Zig
                if node == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if node == p.left and p == gp.left:
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif node == p.right and p == gp.right:
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif node == p.right and p == gp.left:
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif node == p.left and p == gp.right:
                    self._rotate_right(p)
                    self._rotate_left(gp)

    # Optional: for debugging & testing
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res