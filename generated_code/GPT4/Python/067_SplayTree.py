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
        while x.parent:
            if not x.parent.parent:
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
            else:
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        curr = self.root
        parent = None
        while curr:
            parent = curr
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                self._splay(curr)
                return  # Key already exists
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def _find(self, key):
        curr = self.root
        prev = None
        while curr:
            prev = curr
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                return curr
        return None, prev

    def search(self, key):
        curr = self.root
        prev = None
        while curr:
            prev = curr
            if key < curr.key:
                curr = curr.left
            elif key > curr.key:
                curr = curr.right
            else:
                self._splay(curr)
                return True
        if prev:
            self._splay(prev)
        return False

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                break
        else:
            if self.root:
                # If key not found, splay last accessed node to root
                self.search(key)
            return  # Key not found

        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            min_right = self._subtree_minimum(node.right)
            if min_right.parent != node:
                self._replace(min_right, min_right.right)
                min_right.right = node.right
                min_right.right.parent = min_right
            self._replace(node, min_right)
            min_right.left = node.left
            min_right.left.parent = min_right
        # No need to splay after deletion

    # Optional: In-order traversal for debugging
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)

    def to_list(self):
        res = []
        self._inorder(self.root, res)
        return res