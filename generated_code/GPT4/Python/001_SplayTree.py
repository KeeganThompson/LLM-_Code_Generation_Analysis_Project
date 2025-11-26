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

    # Left rotation
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

    # Splaying operation to move x to root
    def _splay(self, x):
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
                else:
                    # x == p.left and p == gp.right
                    # Zig-zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

    def _find(self, key):
        """Find node with key, or last node accessed (parent of where key should be) and a bool if found."""
        node = self.root
        prev = None
        while node:
            prev = node
            if key == node.key:
                return node, True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return prev, False

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
                return  # Key already present, do nothing
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

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def delete(self, key):
        node, found = self._find(key)
        if not found:
            if node:
                self._splay(node)
            return  # Key not found

        self._splay(node)

        # Remove root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find max in left subtree
            y = node.left
            while y.right:
                y = y.right
            if y.parent != node:
                self._replace(y, y.left)
                y.left = node.left
                y.left.parent = y
            self._replace(node, y)
            y.right = node.right
            y.right.parent = y

    def search(self, key):
        node, found = self._find(key)
        # Splay accessed node (found) or its parent (not found, node is parent of where it would be)
        if node:
            self._splay(node)
        return found

    # For debugging and testing
    def _inorder(self, node=None, res=None):
        if res is None:
            res = []
        if node is None:
            node = self.root
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)
        return res

    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        return "SplayTree" + str(self._inorder())