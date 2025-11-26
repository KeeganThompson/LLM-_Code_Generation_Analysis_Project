class SplayTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig step
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-zig step
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-zig step
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-zag step
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
            else:
                # Zig-zag step
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)

    def search(self, key):
        """
        Returns True if key is present, else False.
        Splays the accessed node (or its parent if not found) to the root.
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
        Inserts the key if not present. Splays the inserted node to the root.
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
                return  # already exists, do nothing
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        node = self.Node(key)
        node.parent = parent
        if key < parent.key:
            parent.left = node
        else:
            parent.right = node
        self._splay(node)

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
        Deletes the key if present. Splays the parent of the deleted node (or the deleted node itself if it exists) to the root.
        """
        x = self.root
        while x:
            if key == x.key:
                self._splay(x)
                # Node with two children
                if x.left and x.right:
                    min_right = self._subtree_minimum(x.right)
                    if min_right.parent != x:
                        self._replace(min_right, min_right.right)
                        min_right.right = x.right
                        if min_right.right:
                            min_right.right.parent = min_right
                    self._replace(x, min_right)
                    min_right.left = x.left
                    if min_right.left:
                        min_right.left.parent = min_right
                    self.root = min_right
                    min_right.parent = None
                elif x.left:
                    self._replace(x, x.left)
                elif x.right:
                    self._replace(x, x.right)
                else:
                    self._replace(x, None)
                return
            elif key < x.key:
                if not x.left:
                    self._splay(x)
                    return
                x = x.left
            else:
                if not x.right:
                    self._splay(x)
                    return
                x = x.right

    # Optional: For debugging and testing
    def _inorder(self, node=None):
        if node is None:
            node = self.root
        res = []
        def inorder(x):
            if x:
                inorder(x.left)
                res.append(x.key)
                inorder(x.right)
        inorder(node)
        return res

    # Optional: For testing presence like in a set
    def __contains__(self, key):
        return self.search(key)