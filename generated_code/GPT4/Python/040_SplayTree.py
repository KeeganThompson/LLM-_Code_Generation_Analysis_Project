class SplayTree:
    class Node:
        __slots__ = ('key', 'left', 'right', 'parent')
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None

    # --------- Utility Methods ----------

    def _left_rotate(self, x):
        y = x.right
        if y is None:
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
        if y is None:
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
            if not x.parent.parent:
                # Zig step
                if x.parent.left == x:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-Zig step
                self._right_rotate(x.parent.parent)
                self._right_rotate(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-Zig step
                self._left_rotate(x.parent.parent)
                self._left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-Zag step
                self._right_rotate(x.parent)
                self._left_rotate(x.parent)
            else:
                # Zig-Zag step
                self._left_rotate(x.parent)
                self._right_rotate(x.parent)

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

    # --------- Public Methods ----------

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
                # Key already exists, splay it to root
                self._splay(node)
                return
        new_node = self.Node(key)
        new_node.parent = parent
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
        # Splay the last accessed node (parent where search failed)
        if last:
            self._splay(last)
        return False

    def delete(self, key):
        if not self.search(key):
            return  # Key not found, nothing to delete
        # Now, self.root.key == key
        node = self.root
        if not node.left:
            self._replace(node, node.right)
            if self.root:
                self.root.parent = None
        elif not node.right:
            self._replace(node, node.left)
            if self.root:
                self.root.parent = None
        else:
            # Find minimum of right subtree
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
            min_right.parent = None
            self.root = min_right

    # --------- Optional: Set-like methods ----------

    def __contains__(self, key):
        return self.search(key)

    def __bool__(self):
        return self.root is not None

    def inorder(self):
        # Returns a generator for in-order traversal (for testing/debugging)
        def _inorder(node):
            if node:
                yield from _inorder(node.left)
                yield node.key
                yield from _inorder(node.right)
        yield from _inorder(self.root)