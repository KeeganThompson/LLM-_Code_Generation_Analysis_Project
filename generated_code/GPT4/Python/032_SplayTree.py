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

    # Helper rotate functions
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
        elif x.parent.left is x:
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
        elif x.parent.right is x:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig
                if x.parent.left is x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if p.left is x and g.left is p:
                    # Zig-zig
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif p.right is x and g.right is p:
                    # Zig-zig
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif p.left is x and g.right is p:
                    # Zig-zag
                    self._rotate_right(p)
                    self._rotate_left(g)
                else:  # p.right is x and g.left is p
                    # Zig-zag
                    self._rotate_left(p)
                    self._rotate_right(g)

    def insert(self, key):
        if not self.root:
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
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return True
        # Not found, splay last accessed node (parent of where key would be)
        if last:
            self._splay(last)
        return False

    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found, nothing to delete
        node = self.root  # After search, if found, node to be deleted is at root

        # If no left child, replace root with right child
        if not node.left:
            self._replace_root(node.right)
        # If no right child, replace root with left child
        elif not node.right:
            self._replace_root(node.left)
        else:
            # Both children exist
            # Find max in left subtree
            y = node.left
            while y.right:
                y = y.right
            # Splay y to the root of left subtree
            self._splay(y)
            # Now y is root of left subtree, and has no right child
            y.right = node.right
            if node.right:
                node.right.parent = y
            self._replace_root(y)

    def _replace_root(self, node):
        if node:
            node.parent = None
        self.root = node

    # Optional: For debugging and testing
    def inorder(self):
        res = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return res

    def __contains__(self, key):
        return self.search(key)

    def __iter__(self):
        stack = []
        node = self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key
            node = node.right