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

    # Rotate x up over its parent
    def _rotate(self, x):
        p = x.parent
        if p is None:
            return
        g = p.parent
        if p.left == x:
            # Right rotation
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
            # Left rotation
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p
        p.parent = x
        x.parent = g
        if g:
            if g.left == p:
                g.left = x
            else:
                g.right = x
        else:
            self.root = x

    # Splay x to root
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            p = x.parent
            g = p.parent
            if g is None:
                self._rotate(x)
            elif (g.left == p and p.left == x) or (g.right == p and p.right == x):
                self._rotate(p)
                self._rotate(x)
            else:
                self._rotate(x)
                self._rotate(x)

    def insert(self, key):
        """Insert key if not present."""
        if self.root is None:
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
                self._splay(x)
                return  # Already present, no duplicates
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def search(self, key):
        """Search key and splay accessed node (or last accessed parent) to root. Returns True if found."""
        x = self.root
        prev = None
        while x:
            prev = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self._splay(x)
                return True
        if prev:
            self._splay(prev)
        return False

    def delete(self, key):
        """Delete key if present."""
        if not self.root:
            return
        if not self.search(key):
            return  # Not found; now closest node is at root
        # Now self.root.key == key
        to_delete = self.root
        if not to_delete.left:
            self._replace_root(to_delete.right)
        elif not to_delete.right:
            self._replace_root(to_delete.left)
        else:
            # Find max in left subtree
            max_left = to_delete.left
            while max_left.right:
                max_left = max_left.right
            self._splay(max_left)
            # Now max_left is root, and has no right child
            max_left.right = to_delete.right
            if to_delete.right:
                to_delete.right.parent = max_left
            self.root = max_left
            max_left.parent = None
        # Python's GC will collect to_delete

    def _replace_root(self, node):
        self.root = node
        if node:
            node.parent = None

    # Optional: For debugging
    def _inorder(self, node=None):
        if node is None:
            node = self.root
        if node:
            yield from self._inorder(node.left)
            yield node.key
            yield from self._inorder(node.right)

    # To mimic a set interface (optional)
    def __contains__(self, key):
        return self.search(key)

    def __iter__(self):
        return self._inorder()

    def __bool__(self):
        return self.root is not None