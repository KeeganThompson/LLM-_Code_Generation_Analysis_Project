class SplayTree:
    class Node:
        __slots__ = ('key', 'left', 'right', 'parent')
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
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
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
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    # Splaying operation
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
            elif x == x.parent.left and x.parent == x.parent.parent.right:
                # Zig-Zag
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
            else:
                # Zig-Zag
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)

    # Internal: Find node with key, return (found_node, parent_of_last_visited)
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
                return x, prev
        return None, prev

    # Public: Search and splay
    def search(self, key):
        node, parent = self._find(key)
        splay_node = node if node else parent
        if splay_node:
            self._splay(splay_node)
        return node is not None

    # Public: Insert key
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
                # Key already exists, splay it
                self._splay(x)
                return
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    # Public: Delete key
    def delete(self, key):
        node, parent = self._find(key)
        if not node:
            # Key not found, splay the last accessed node (parent)
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

    # Internal: Replace u with v in the parent
    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        else:
            if u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
        if v:
            v.parent = u.parent

    # For debugging: inorder traversal
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res

# Example usage:
# s = SplayTree()
# s.insert(5)
# s.insert(3)
# s.insert(8)
# print(s.search(3))  # True
# s.delete(5)
# print(s.inorder())  # [3,8]