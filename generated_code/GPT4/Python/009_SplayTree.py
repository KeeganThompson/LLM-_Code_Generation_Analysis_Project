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
        if not x:
            return
        while x.parent:
            if not x.parent.parent:
                # Zig step
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                gp = p.parent
                if x == p.left and p == gp.left:
                    # Zig-zig step
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif x == p.right and p == gp.right:
                    # Zig-zig step
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif x == p.right and p == gp.left:
                    # Zig-zag step
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif x == p.left and p == gp.right:
                    # Zig-zag step
                    self._rotate_right(p)
                    self._rotate_left(gp)

    def search(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key == x.key:
                self._splay(x)
                return True
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        # Splay last accessed node (parent of not-found node)
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        x = self.root
        parent = None
        while x:
            parent = x
            if key == x.key:
                self._splay(x)
                return  # Already in tree, do nothing
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def _subtree_minimum(self, x):
        while x.left:
            x = x.left
        return x

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
        if not node or node.key != key:
            if node:
                self._splay(node)
            return  # Key not found; do nothing

        # Now node is at root
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
                min_right.right.parent = min_right
            self._replace(node, min_right)
            min_right.left = node.left
            min_right.left.parent = min_right
        # No need to explicitly delete node; garbage collector will clean up

    # For debugging: in-order traversal as a sorted list
    def to_list(self):
        def inorder(x):
            if not x:
                return []
            return inorder(x.left) + [x.key] + inorder(x.right)
        return inorder(self.root)