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

    # Right rotate
    def _right_rotate(self, x):
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

    # Left rotate
    def _left_rotate(self, x):
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

    # Splaying operation: brings x to the root
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            if x.parent.parent is None:
                # Zig step
                if x == x.parent.left:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-Zig step
                self._right_rotate(x.parent.parent)
                self._right_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-Zig step
                self._left_rotate(x.parent.parent)
                self._left_rotate(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-Zag step
                self._left_rotate(x.parent)
                self._right_rotate(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.right:
                # Zig-Zag step
                self._right_rotate(x.parent)
                self._left_rotate(x.parent)

    # Internal search: returns (node, last_accessed_parent)
    def _find(self, key):
        node = self.root
        prev = None
        while node:
            prev = node
            if key == node.key:
                return node, prev
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None, prev

    # Public search: splay the node or its parent to root
    def search(self, key):
        node, last = self._find(key)
        if node:
            self._splay(node)
            return True
        elif last:
            self._splay(last)
        return False

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
                return  # No duplicates in set
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

    def delete(self, key):
        found, _ = self._find(key)
        if not found:
            if _:
                self._splay(_)
            return  # Key not found
        self._splay(found)
        # Now found is at root
        if found.left:
            left_subtree = found.left
            left_subtree.parent = None
            # Find max in left subtree
            max_left = left_subtree
            while max_left.right:
                max_left = max_left.right
            self._splay(max_left)
            # Now max_left is new root, attach right subtree
            max_left.right = found.right
            if found.right:
                found.right.parent = max_left
            self.root = max_left
        elif found.right:
            found.right.parent = None
            self.root = found.right
        else:
            self.root = None
        # Help GC
        found.left = found.right = found.parent = None

    # For debugging: inorder traversal
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)
    def keys(self):
        res = []
        self._inorder(self.root, res)
        return res

    # For checking containment
    def __contains__(self, key):
        return self.search(key)

    # For adding with set-like syntax
    def add(self, key):
        self.insert(key)

    # For removing with set-like syntax
    def remove(self, key):
        self.delete(key)