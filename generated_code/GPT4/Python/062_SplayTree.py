class SplayTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None

    def _left_rotate(self, x):
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

    def _right_rotate(self, x):
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

    def _splay(self, x):
        if not x:
            return
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:
                # Zig
                if x == p.left:
                    self._right_rotate(p)
                else:
                    self._left_rotate(p)
            else:
                if x == p.left and p == gp.left:
                    # Zig-zig
                    self._right_rotate(gp)
                    self._right_rotate(p)
                elif x == p.right and p == gp.right:
                    # Zig-zig
                    self._left_rotate(gp)
                    self._left_rotate(p)
                elif x == p.right and p == gp.left:
                    # Zig-zag
                    self._left_rotate(p)
                    self._right_rotate(gp)
                else:
                    # x == p.left and p == gp.right
                    self._right_rotate(p)
                    self._left_rotate(gp)

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

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        while True:
            if key == node.key:
                self._splay(node)
                return  # Already present, do nothing
            elif key < node.key:
                if node.left:
                    node = node.left
                else:
                    new_node = self.Node(key)
                    node.left = new_node
                    new_node.parent = node
                    self._splay(new_node)
                    return
            else:
                if node.right:
                    node = node.right
                else:
                    new_node = self.Node(key)
                    node.right = new_node
                    new_node.parent = node
                    self._splay(new_node)
                    return

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def delete(self, key):
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
            # Key not found, splay last accessed node (if any)
            if self.root:
                self.search(key)
            return

        # node is at root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Both children exist
            min_right = self._subtree_minimum(node.right)
            if min_right.parent != node:
                self._replace(min_right, min_right.right)
                min_right.right = node.right
                if min_right.right:
                    min_right.right.parent = min_right
            self._replace(node, min_right)
            min_right.left = node.left
            if min_right.left:
                min_right.left.parent = min_right

    # Optional: for debugging (not required by the prompt)
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res