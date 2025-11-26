class SplayTree:
    class Node:
        __slots__ = 'key', 'left', 'right', 'parent'
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Helper: Rotate x up
    def _rotate(self, x):
        p = x.parent
        if p is None:
            return  # x is root
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

    # Splaying x to root (or closest possible if x is None)
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                self._rotate(x)
            elif (g.left == p) == (p.left == x):  # Zig-zig
                self._rotate(p)
                self._rotate(x)
            else:  # Zig-zag
                self._rotate(x)
                self._rotate(x)

    # Search for key, splay the found node (or last accessed node) to root
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

    # Insert key (if not present), splay new node to root
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
                return  # Already exists, do nothing
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        newnode = self.Node(key, parent)
        if key < parent.key:
            parent.left = newnode
        else:
            parent.right = newnode
        self._splay(newnode)

    # Find node with key
    def _find(self, key):
        node = self.root
        last = None
        while node:
            last = node
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    # Join two trees: left's all keys < right's all keys
    def _join(self, left, right):
        if not left:
            return right
        if not right:
            return left
        # Max of left
        node = left
        while node.right:
            node = node.right
        self._splay_node(node, left)
        node.right = right
        if right:
            right.parent = node
        return node

    # Splay node x, given a custom root
    def _splay_node(self, x, root):
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                self._rotate_custom(x, root)
            elif (g.left == p) == (p.left == x):  # Zig-zig
                self._rotate_custom(p, root)
                self._rotate_custom(x, root)
            else:  # Zig-zag
                self._rotate_custom(x, root)
                self._rotate_custom(x, root)

    def _rotate_custom(self, x, root):
        p = x.parent
        if p is None:
            return
        g = p.parent

        if p.left == x:
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
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
        # else: do not update self.root

    # Delete key if present. Splay the parent of deleted node (or root) to root.
    def delete(self, key):
        node = self.root
        parent = None
        while node:
            if key == node.key:
                break
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        if not node:
            if parent:
                self._splay(parent)
            return  # Not found
        self._splay(node)
        # Now node is root
        left = node.left
        right = node.right
        if left:
            left.parent = None
        if right:
            right.parent = None
        # Join left and right as new tree
        self.root = self._join(left, right)

    # For debugging: inorder traversal
    def _inorder(self, node, res):
        if not node:
            return
        self._inorder(node.left, res)
        res.append(node.key)
        self._inorder(node.right, res)

    # Return sorted list of keys
    def keys(self):
        res = []
        self._inorder(self.root, res)
        return res