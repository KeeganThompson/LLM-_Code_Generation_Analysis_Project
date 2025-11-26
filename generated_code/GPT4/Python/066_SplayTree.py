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
        if p is None:
            return
        g = p.parent

        if p.left == x:
            # Right rotation
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
            # Left rotation
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p

        p.parent = x
        x.parent = g

        if g:
            if g.left == p:
                g.left = x
            else:
                g.right = x
        else:
            self.root = x

    # Splay x to the root
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            p = x.parent
            g = p.parent
            if g is None:
                # Zig
                self._rotate(x)
            elif (g.left == p and p.left == x) or (g.right == p and p.right == x):
                # Zig-zig
                self._rotate(p)
                self._rotate(x)
            else:
                # Zig-zag
                self._rotate(x)
                self._rotate(x)

    # Insert key if not present
    def insert(self, key):
        if self.root is None:
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
                # Already present, splay it
                self._splay(x)
                return

        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    # Find node with key, return node and last accessed parent if not found
    def _find(self, key):
        x = self.root
        prev = None
        while x:
            prev = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x, None
        return None, prev

    # Search key and splay accessed node (or last accessed parent) to root
    def search(self, key):
        node, parent = self._find(key)
        if node:
            self._splay(node)
            return True
        elif parent:
            self._splay(parent)
            return False
        return False

    # Join two trees: all keys in left < all keys in right
    def _join(self, left, right):
        if not left:
            return right
        x = left
        while x.right:
            x = x.right
        self._splay(x)
        x.right = right
        if right:
            right.parent = x
        return x

    # Delete key from tree
    def delete(self, key):
        node, parent = self._find(key)
        if node is None:
            if parent:
                self._splay(parent)
            return False
        self._splay(node)
        left = node.left
        right = node.right
        if left:
            left.parent = None
        if right:
            right.parent = None
        self.root = self._join(left, right)
        return True

    # For debugging: In-order traversal
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

    # For debugging: Check if key exists
    def __contains__(self, key):
        found = self.search(key)
        return found

    # For debugging: String representation
    def __str__(self):
        return "SplayTree" + str(self._inorder())