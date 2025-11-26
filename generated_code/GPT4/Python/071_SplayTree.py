class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Rotate node x to the right
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

    # Rotate node x to the left
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

    # Splay node x to root
    def _splay(self, x):
        while x.parent:
            if x.parent.parent is None:
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
            else:
                # x == x.parent.left and x.parent == x.parent.parent.right
                # Zig-Zag
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

    # Find node with key, return node and its parent (if not found, parent is where it would be inserted)
    def _find(self, key):
        node = self.root
        parent = None
        while node:
            if key == node.key:
                return node, parent
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        return None, parent

    # Public search: splay accessed node or its parent if not found
    def search(self, key):
        node = self.root
        parent = None
        while node:
            if key == node.key:
                self._splay(node)
                return True
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        if parent:
            self._splay(parent)
        return False

    # Public insert
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
                return  # Already in set
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

    # Public delete
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
            # Not found, splay parent if possible
            parent = None
            node = self.root
            while node:
                parent = node
                if key < node.key:
                    node = node.left
                else:
                    node = node.right
            if parent:
                self._splay(parent)
            return  # Key not found

        # node is now root
        if node.left is None:
            self._replace(node, node.right)
        elif node.right is None:
            self._replace(node, node.left)
        else:
            # Find max in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            if max_left.parent != node:
                self._replace(max_left, max_left.left)
                max_left.left = node.left
                max_left.left.parent = max_left
            self._replace(node, max_left)
            max_left.right = node.right
            max_left.right.parent = max_left

    # Helper to replace subtree u with v
    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # For debugging: inorder traversal
    def inorder(self):
        def _inorder(node):
            if node:
                yield from _inorder(node.left)
                yield node.key
                yield from _inorder(node.right)
        return list(_inorder(self.root))

    # For debugging: check if key is in the tree
    def __contains__(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False