class SplayTree:
    class Node:
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
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        if y:
            y.right = x
        x.parent = y

    # Left rotation
    def _rotate_left(self, x):
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        if not x.parent:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        if y:
            y.left = x
        x.parent = y

    # Splaying operation
    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                if x.parent.left == x and x.parent.parent.left == x.parent:
                    # Zig-zig
                    self._rotate_right(x.parent.parent)
                    self._rotate_right(x.parent)
                elif x.parent.right == x and x.parent.parent.right == x.parent:
                    # Zig-zig
                    self._rotate_left(x.parent.parent)
                    self._rotate_left(x.parent)
                elif x.parent.left == x and x.parent.parent.right == x.parent:
                    # Zig-zag
                    self._rotate_right(x.parent)
                    self._rotate_left(x.parent)
                else:
                    # Zig-zag
                    self._rotate_left(x.parent)
                    self._rotate_right(x.parent)

    # Find node with key, and splay it if found.
    # If not found, splay the parent of the last accessed node.
    def search(self, key):
        x = self.root
        prev = None
        while x:
            prev = x
            if key == x.key:
                self._splay(x)
                return True
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        if prev:
            self._splay(prev)
        return False

    # Insert key if not present
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
                return  # Key already exists
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

    # Find node with a given key
    def _find_node(self, key):
        x = self.root
        while x:
            if key == x.key:
                return x
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        return None

    # Replace u with v in the tree
    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Find maximum node in subtree
    def _subtree_maximum(self, x):
        while x.right:
            x = x.right
        return x

    # Delete key if present
    def delete(self, key):
        node = self._find_node(key)
        if not node:
            # Splay the last accessed node (as in search)
            self.search(key)
            return  # Key not found, nothing to do
        self._splay(node)
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Both children exist
            y = self._subtree_maximum(node.left)
            if y.parent != node:
                self._replace(y, y.left)
                y.left = node.left
                y.left.parent = y
            self._replace(node, y)
            y.right = node.right
            y.right.parent = y
        # Node is deleted

    # Optional: for debugging purposes
    def inorder(self):
        def _inorder(x):
            if not x:
                return []
            return _inorder(x.left) + [x.key] + _inorder(x.right)
        return _inorder(self.root)