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

    # ---------- Rotation helpers ----------
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
            if x == x.parent.left:
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
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y

    # ---------- Splay operation ----------
    def _splay(self, x):
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:  # Zig
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if x == p.left and p == gp.left:
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif x == p.right and p == gp.right:
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif x == p.right and p == gp.left:
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif x == p.left and p == gp.right:
                    self._rotate_right(p)
                    self._rotate_left(gp)

    # ---------- Search with splay ----------
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

    # ---------- Insert ----------
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

    # ---------- Delete ----------
    def delete(self, key):
        if not self.search(key):
            return  # Key not found, nothing to delete

        node = self.root  # After search, node with key is at root
        # Remove root
        if node.left is None:
            self._replace_root(node.right)
        elif node.right is None:
            self._replace_root(node.left)
        else:
            # Find max in left subtree
            left_subtree = node.left
            left_subtree.parent = None
            max_left = left_subtree
            while max_left.right:
                max_left = max_left.right
            self._splay_node_in_subtree(max_left, left_subtree)
            # Now max_left is new root of left subtree
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self.root = max_left
            max_left.parent = None

    def _replace_root(self, node):
        self.root = node
        if node:
            node.parent = None

    def _splay_node_in_subtree(self, node, subtree_root):
        # Splay node to root of subtree (used in delete)
        while node.parent:
            if node.parent == subtree_root:
                if node == node.parent.left:
                    self._rotate_right(node.parent)
                else:
                    self._rotate_left(node.parent)
            else:
                p = node.parent
                gp = p.parent
                if node == p.left and p == gp.left:
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif node == p.right and p == gp.right:
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif node == p.right and p == gp.left:
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif node == p.left and p == gp.right:
                    self._rotate_right(p)
                    self._rotate_left(gp)

    # ---------- Utility ----------
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

    def __len__(self):
        def count(node):
            if not node:
                return 0
            return 1 + count(node.left) + count(node.right)
        return count(self.root)