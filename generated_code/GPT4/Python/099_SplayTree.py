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

    def _rotate_right(self, x):
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
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:
                # Zig
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if x == p.left and p == gp.left:
                    # Zig-Zig
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif x == p.right and p == gp.right:
                    # Zig-Zig
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif x == p.right and p == gp.left:
                    # Zig-Zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif x == p.left and p == gp.right:
                    # Zig-Zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

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
        parent = None
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return  # key already exists
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

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

    def delete(self, key):
        if not self.root:
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
            # Key not found, splay last accessed node
            if node is not None:
                self._splay(node)
            return

        # Now node is root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Both children exist
            min_node = self._subtree_minimum(node.right)
            if min_node.parent != node:
                self._replace(min_node, min_node.right)
                min_node.right = node.right
                if min_node.right:
                    min_node.right.parent = min_node
            self._replace(node, min_node)
            min_node.left = node.left
            if min_node.left:
                min_node.left.parent = min_node
        # Python GC will clean up node

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: For debugging
    def __contains__(self, key):
        return self.search(key)

    def __repr__(self):
        lines = []
        def _print(node, level=0):
            if node:
                _print(node.right, level + 1)
                lines.append('   ' * level + str(node.key))
                _print(node.left, level + 1)
        _print(self.root)
        return '\n'.join(lines)