class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # ======== Utility Rotation Methods ========

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
        elif x.parent.left == x:
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
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    # ======== Splaying ========

    def _splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                # Zig step
                if p.left == x:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if g.left == p and p.left == x:
                    # Zig-zig step
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif g.right == p and p.right == x:
                    # Zig-zig step
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif g.left == p and p.right == x:
                    # Zig-zag step
                    self._rotate_left(p)
                    self._rotate_right(g)
                elif g.right == p and p.left == x:
                    # Zig-zag step
                    self._rotate_right(p)
                    self._rotate_left(g)

    # ======== Search ========

    def search(self, key):
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
        # Splay the last accessed node (prev), which is the parent if not found
        if prev:
            self._splay(prev)
        return False

    # ======== Insert ========

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
                return  # Key already exists, do nothing
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

    # ======== Delete ========

    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found, nothing to delete
        # Now, self.root is the node to delete
        node = self.root
        if not node.left:
            self._replace_root(node.right)
        elif not node.right:
            self._replace_root(node.left)
        else:
            # Find the maximum node in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            # Splay max_left to root of left subtree
            self._splay(max_left)
            # Now, max_left is the new left-root (no right child)
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self._replace_root(max_left)

    def _replace_root(self, node):
        if node:
            node.parent = None
        self.root = node

    # ======== For Testing/Debug (Optional) ========

    def inorder(self):
        res = []
        def _inorder(n):
            if n:
                _inorder(n.left)
                res.append(n.key)
                _inorder(n.right)
        _inorder(self.root)
        return res

    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        # Simple level-order traversal for visualization
        if not self.root:
            return "<empty>"
        result = []
        q = [(self.root, 0)]
        current_level = 0
        current_line = []
        while q:
            node, level = q.pop(0)
            if level != current_level:
                result.append(' '.join(current_line))
                current_line = []
                current_level = level
            current_line.append(str(node.key))
            if node.left:
                q.append((node.left, level + 1))
            if node.right:
                q.append((node.right, level + 1))
        if current_line:
            result.append(' '.join(current_line))
        return '\n'.join(result)