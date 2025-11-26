class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # ----------- Splay operations -----------

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
        while x.parent is not None:
            p = x.parent
            gp = p.parent
            if gp is None:
                # Zig
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            elif x == p.left and p == gp.left:
                # Zig-zig
                self._rotate_right(gp)
                self._rotate_right(p)
            elif x == p.right and p == gp.right:
                # Zig-zig
                self._rotate_left(gp)
                self._rotate_left(p)
            elif x == p.right and p == gp.left:
                # Zig-zag
                self._rotate_left(p)
                self._rotate_right(gp)
            elif x == p.left and p == gp.right:
                # Zig-zag
                self._rotate_right(p)
                self._rotate_left(gp)

    # ----------- Search -----------

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

    # ----------- Insert -----------

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
                return  # Already in tree, do nothing
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

    # ----------- Delete -----------

    def delete(self, key):
        if not self.root:
            return
        node = self.root
        while node:
            if key == node.key:
                self._splay(node)
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        else:
            if node is None:
                return  # Key not found

        # Now node is at root
        if self.root.left is None:
            self._replace(self.root, self.root.right)
        elif self.root.right is None:
            self._replace(self.root, self.root.left)
        else:
            # Find max in left subtree
            max_node = self.root.left
            while max_node.right:
                max_node = max_node.right
            if max_node.parent != self.root:
                self._replace(max_node, max_node.left)
                max_node.left = self.root.left
                if max_node.left:
                    max_node.left.parent = max_node
            self._replace(self.root, max_node)
            max_node.right = self.root.right
            if max_node.right:
                max_node.right.parent = max_node
            max_node.parent = None
            self.root = max_node

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # ----------- Utility -----------

    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        def _traverse(node):
            if not node:
                return []
            return _traverse(node.left) + [node.key] + _traverse(node.right)
        return "{" + ", ".join(map(str, _traverse(self.root))) + "}"

# Example usage:
# tree = SplayTree()
# tree.insert(5)
# tree.insert(3)
# tree.insert(8)
# print(tree.search(3)) # True
# print(tree.search(7)) # False
# tree.delete(5)
# print(tree)