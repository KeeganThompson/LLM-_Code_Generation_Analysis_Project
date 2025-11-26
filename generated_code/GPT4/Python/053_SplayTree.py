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
        if y is None:
            return
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        else:
            if x.parent.left is x:
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
        else:
            if x.parent.left is x:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            p = x.parent
            gp = p.parent
            if gp is None:
                # Zig
                if p.left is x:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if gp.left is p and p.left is x:
                    # Zig-zig
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif gp.right is p and p.right is x:
                    # Zig-zig
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif gp.left is p and p.right is x:
                    # Zig-zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif gp.right is p and p.left is x:
                    # Zig-zag
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
        if self.root is None:
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
        new_node = self.Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def delete(self, key):
        if not self.search(key):
            return  # Key not found
        node = self.root
        # Now node.key == key
        if node.left is None:
            self._replace_root(node.right)
        elif node.right is None:
            self._replace_root(node.left)
        else:
            # Both children exist
            # Find max in left subtree
            left_subtree = node.left
            left_subtree.parent = None
            max_left = left_subtree
            while max_left.right:
                max_left = max_left.right
            self._splay_in_subtree(max_left, left_subtree)
            # Now, max_left is root of left_subtree, and has no right child
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self.root = max_left
            max_left.parent = None

    def _replace_root(self, node):
        self.root = node
        if node:
            node.parent = None

    def _splay_in_subtree(self, x, subtree_root):
        # Splay x to the root of its (sub)tree (not the main root)
        while x.parent:
            p = x.parent
            gp = p.parent
            if gp is None or gp is not subtree_root:
                if p.left is x:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if gp.left is p and p.left is x:
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif gp.right is p and p.right is x:
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif gp.left is p and p.right is x:
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif gp.right is p and p.left is x:
                    self._rotate_right(p)
                    self._rotate_left(gp)
        if x.parent is None:
            # x is now root of subtree
            pass

    # For debugging: inorder traversal
    def inorder(self):
        def _inorder(node):
            if node:
                yield from _inorder(node.left)
                yield node.key
                yield from _inorder(node.right)
        return list(_inorder(self.root))

    # For debugging: check if key is in tree
    def __contains__(self, key):
        return self.search(key)