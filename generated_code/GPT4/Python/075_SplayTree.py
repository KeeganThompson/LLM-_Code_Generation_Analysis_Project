class SplayTree:
    class Node:
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
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-zig step
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-zig step
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-zag step
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)
            else:
                # Zig-zag step
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

    def search(self, key):
        """
        Searches for the key.
        If found, splays the node to the root and returns True.
        If not found, splays the last accessed node (parent of where it would be) to the root and returns False.
        """
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
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        """
        Inserts key into the set.
        If key already exists, does nothing.
        Splays the inserted or existing node to the root.
        """
        if not self.root:
            self.root = self.Node(key)
            return

        x = self.root
        parent = None
        while x:
            parent = x
            if key == x.key:
                self._splay(x)
                return
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
        """
        Deletes key from the set if present.
        Splays the parent of the deleted node (or root in degenerate cases) to the root.
        """
        if not self.root:
            return

        x = self.root
        parent = None
        while x:
            if key == x.key:
                break
            parent = x
            if key < x.key:
                x = x.left
            else:
                x = x.right

        if not x:
            if parent:
                self._splay(parent)
            return  # Key not found

        self._splay(x)  # Splay node to be deleted to root

        # Remove the root
        if not x.left:
            self._replace(x, x.right)
            if self.root:
                self._splay(self.root)
        elif not x.right:
            self._replace(x, x.left)
            if self.root:
                self._splay(self.root)
        else:
            # Both children exist
            y = self._subtree_minimum(x.right)
            if y.parent != x:
                self._replace(y, y.right)
                y.right = x.right
                y.right.parent = y
            self._replace(x, y)
            y.left = x.left
            y.left.parent = y
            self._splay(y)

    # Optional: For debugging or visualization
    def _inorder(self, x, res):
        if x:
            self._inorder(x.left, res)
            res.append(x.key)
            self._inorder(x.right, res)

    def to_list(self):
        res = []
        self._inorder(self.root, res)
        return res