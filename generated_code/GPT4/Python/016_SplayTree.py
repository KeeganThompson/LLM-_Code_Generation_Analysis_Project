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

    # ====== Rotation helpers ======
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
        elif x.parent.left is x:
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
        elif x.parent.right is x:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # ====== Splaying ======
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:
                # Zig
                if p.left is x:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if gp.left is p and p.left is x:
                    # Zig-Zig
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif gp.right is p and p.right is x:
                    # Zig-Zig
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif gp.left is p and p.right is x:
                    # Zig-Zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif gp.right is p and p.left is x:
                    # Zig-Zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

    # ====== Insertion ======
    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        x = self.root
        while True:
            if key == x.key:
                self._splay(x)
                return
            elif key < x.key:
                if x.left:
                    x = x.left
                else:
                    x.left = self.Node(key, parent=x)
                    self._splay(x.left)
                    return
            else:
                if x.right:
                    x = x.right
                else:
                    x.right = self.Node(key, parent=x)
                    self._splay(x.right)
                    return

    # ====== Search with Splay ======
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

    # ====== Deletion ======
    def delete(self, key):
        if self.root is None:
            return
        # First, search (and splay) the node to root
        found = self.search(key)
        if not found:
            return
        # Now self.root.key == key
        if self.root.left is None:
            self._replace_root(self.root.right)
        elif self.root.right is None:
            self._replace_root(self.root.left)
        else:
            # Both children exist
            # Find max in left subtree
            left_subtree = self.root.left
            left_subtree.parent = None
            max_node = left_subtree
            while max_node.right:
                max_node = max_node.right
            # Splay the max node of left subtree to the root of left subtree
            self._splay_node_to_root(left_subtree, max_node)
            # Now max_node is root of left subtree, attach right subtree
            max_node.right = self.root.right
            if max_node.right:
                max_node.right.parent = max_node
            self._replace_root(max_node)

    def _replace_root(self, node):
        self.root = node
        if self.root:
            self.root.parent = None

    def _splay_node_to_root(self, subtree_root, x):
        # Splay x to root in the subtree rooted at subtree_root
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:
                if p.left is x:
                    # right rotation
                    p.left = x.right
                    if x.right:
                        x.right.parent = p
                    x.right = p
                    x.parent = None
                    p.parent = x
                else:
                    # left rotation
                    p.right = x.left
                    if x.left:
                        x.left.parent = p
                    x.left = p
                    x.parent = None
                    p.parent = x
                # After this, x is root of the subtree
                break
            else:
                if gp.left is p and p.left is x:
                    # Zig-Zig right
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif gp.right is p and p.right is x:
                    # Zig-Zig left
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif gp.left is p and p.right is x:
                    # Zig-Zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif gp.right is p and p.left is x:
                    # Zig-Zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

    # ====== Optional: For debugging ======
    def __contains__(self, key):
        return self.search(key)

    def inorder(self):
        def _inorder(x):
            if x:
                yield from _inorder(x.left)
                yield x.key
                yield from _inorder(x.right)
        return list(_inorder(self.root))