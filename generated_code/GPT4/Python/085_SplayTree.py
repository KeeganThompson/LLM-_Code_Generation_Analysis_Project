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

    # ----------- Splaying Operations -----------
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
            if x.parent.parent is None:
                # Zig step
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if x == p.left and p == g.left:
                    # Zig-zig step
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif x == p.right and p == g.right:
                    # Zig-zig step
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif x == p.right and p == g.left:
                    # Zig-zag step
                    self._rotate_left(p)
                    self._rotate_right(g)
                elif x == p.left and p == g.right:
                    # Zig-zag step
                    self._rotate_right(p)
                    self._rotate_left(g)

    # ----------- Public API -----------
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
                # Key already exists, splay it
                self._splay(node)
                return
        new_node = self.Node(key, parent)
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
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        # Key not found, splay the last accessed node (parent)
        if last:
            self._splay(last)
        return False

    def delete(self, key):
        if self.root is None:
            return
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
            # Key not found; nothing to delete
            return
        # Now, node is at root and node.key == key
        if node.left is None:
            self._replace_node(node, node.right)
        elif node.right is None:
            self._replace_node(node, node.left)
        else:
            # Find max in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            if max_left.parent != node:
                self._replace_node(max_left, max_left.left)
                max_left.left = node.left
                if max_left.left:
                    max_left.left.parent = max_left
            self._replace_node(node, max_left)
            max_left.right = node.right
            if max_left.right:
                max_left.right.parent = max_left

    # ----------- Helper Methods -----------
    def _replace_node(self, old, new):
        if old.parent is None:
            self.root = new
        else:
            if old == old.parent.left:
                old.parent.left = new
            else:
                old.parent.right = new
        if new:
            new.parent = old.parent

    # ----------- Optional: For Testing/Debugging -----------
    def inorder(self):
        def _inorder(node):
            if node:
                yield from _inorder(node.left)
                yield node.key
                yield from _inorder(node.right)
        return list(_inorder(self.root))