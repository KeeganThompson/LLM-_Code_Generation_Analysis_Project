class SplayTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None

    # Right rotation
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

    # Left rotation
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

    # Splaying operation
    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig
                if x.parent.left == x:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-Zig
                self._right_rotate(x.parent.parent)
                self._right_rotate(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-Zig
                self._left_rotate(x.parent.parent)
                self._left_rotate(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-Zag
                self._right_rotate(x.parent)
                self._left_rotate(x.parent)
            else:
                # Zig-Zag
                self._left_rotate(x.parent)
                self._right_rotate(x.parent)

    # Search for a key, splay accessed node or its parent to root
    def search(self, key):
        node = self.root
        prev = None
        while node:
            prev = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return True
        if prev:
            self._splay(prev)
        return False

    # Insert a key
    def insert(self, key):
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return  # Key already exists
        new_node = self.Node(key)
        new_node.parent = parent
        if not parent:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    # Find minimum node in subtree
    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

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

    # Delete a key
    def delete(self, key):
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                if not node.left:
                    self._replace(node, node.right)
                elif not node.right:
                    self._replace(node, node.left)
                else:
                    # Find minimum in right subtree
                    min_right = self._subtree_minimum(node.right)
                    if min_right.parent != node:
                        self._replace(min_right, min_right.right)
                        min_right.right = node.right
                        min_right.right.parent = min_right
                    self._replace(node, min_right)
                    min_right.left = node.left
                    min_right.left.parent = min_right
                return
        # If key was not found, splay the last accessed node
        if self.root:
            self.search(key)

    # Optional: for testing (in-order traversal)
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res