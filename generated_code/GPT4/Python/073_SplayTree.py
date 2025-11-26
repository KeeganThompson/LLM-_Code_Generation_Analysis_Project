class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Rotate left at node x
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

    # Rotate right at node x
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

    # Splay node x to root
    def _splay(self, x):
        if not x:
            return
        while x.parent:
            if not x.parent.parent:
                # Zig
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-Zig
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-Zig
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-Zag
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.right:
                # Zig-Zag
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

    # Find node with key, return (node, parent)
    def _find(self, key):
        x = self.root
        parent = None
        while x:
            parent = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x, parent
        return None, parent

    def search(self, key):
        node, parent = self._find(key)
        if node:
            self._splay(node)
            return True
        elif parent:
            self._splay(parent)
            return False
        else:
            return False

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        x = self.root
        parent = None
        while x:
            parent = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                # Key already in set, splay to root
                self._splay(x)
                return
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def delete(self, key):
        node, parent = self._find(key)
        if not node:
            if parent:
                self._splay(parent)
            return
        self._splay(node)
        # Now node is root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Find min of right subtree
            min_node = node.right
            while min_node.left:
                min_node = min_node.left
            if min_node.parent != node:
                self._replace(min_node, min_node.right)
                min_node.right = node.right
                if min_node.right:
                    min_node.right.parent = min_node
            self._replace(node, min_node)
            min_node.left = node.left
            if min_node.left:
                min_node.left.parent = min_node

    # Replace node u with node v in the tree
    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: For debugging and testing
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res

    # Optional: For debugging and testing
    def __contains__(self, key):
        return self.search(key)