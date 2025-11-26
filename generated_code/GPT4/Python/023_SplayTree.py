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

    # ========= Splay Operations =========
    def _left_rotate(self, x):
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

    def _right_rotate(self, x):
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

    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig step
                if x.parent.left == x:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            else:
                p = x.parent
                g = p.parent
                if p.left == x and g.left == p:
                    # Zig-zig step
                    self._right_rotate(g)
                    self._right_rotate(p)
                elif p.right == x and g.right == p:
                    # Zig-zig step
                    self._left_rotate(g)
                    self._left_rotate(p)
                elif p.left == x and g.right == p:
                    # Zig-zag step
                    self._right_rotate(p)
                    self._left_rotate(g)
                else:
                    # Zig-zag step
                    self._left_rotate(p)
                    self._right_rotate(g)

    # ========= Public Methods =========

    def search(self, key):
        """
        Search for key in the splay tree.
        If found, splay node to root and return True.
        If not found, splay last accessed node (parent or last node) to root and return False.
        """
        node = self.root
        prev = None
        while node:
            prev = node
            if key == node.key:
                self._splay(node)
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        if prev:
            self._splay(prev)
        return False

    def insert(self, key):
        """
        Insert key into the splay tree if not already present, and splay the inserted/found node.
        """
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return
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
        """
        Delete key from the splay tree.
        Splay the node with the key to be deleted to the root. 
        If not found, splay the last accessed node.
        """
        if not self.root:
            return
        # First splay the node with key (or closest parent)
        node = self.root
        prev = None
        while node:
            prev = node
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        if not node or node.key != key:
            if prev:
                self._splay(prev)
            return  # Key not found
        self._splay(node)
        # Now node is at root
        if not node.left:
            self._replace_root(node.right)
        elif not node.right:
            self._replace_root(node.left)
        else:
            # Find maximum in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            # Splay max_left to be the new root of left subtree
            self._splay(max_left)
            # Attach right subtree
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self._replace_root(max_left)
        # Remove all links from the deleted node
        node.left = node.right = node.parent = None

    def _replace_root(self, node):
        self.root = node
        if node:
            node.parent = None

    # For debugging and testing
    def inorder(self):
        """Return inorder traversal as list."""
        res = []
        def _inorder(n):
            if not n:
                return
            _inorder(n.left)
            res.append(n.key)
            _inorder(n.right)
        _inorder(self.root)
        return res

    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        """Simple tree display."""
        if not self.root:
            return "<empty>"
        lines = []
        def _print(node, prefix=""):
            if node.right:
                _print(node.right, prefix + "    ")
            lines.append(f"{prefix}{node.key}")
            if node.left:
                _print(node.left, prefix + "    ")
        _print(self.root)
        return "\n".join(lines)