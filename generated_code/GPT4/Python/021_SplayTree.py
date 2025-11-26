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
            p = x.parent
            gp = p.parent
            if not gp:
                # Zig
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if x == p.left and p == gp.left:
                    # Zig-zig
                    self._rotate_right(gp)
                    self._rotate_right(p)
                elif x == p.right and p == gp.right:
                    # Zig-zig
                    self._rotate_left(gp)
                    self._rotate_left(p)
                elif x == p.right and p == gp.left:
                    # Zig-zag
                    self._rotate_left(p)
                    self._rotate_right(gp)
                elif x == p.left and p == gp.right:
                    # Zig-zag
                    self._rotate_right(p)
                    self._rotate_left(gp)

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
        # Splay the last accessed node (parent)
        if prev:
            self._splay(prev)
        return False

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        while True:
            if key == node.key:
                self._splay(node)
                return
            elif key < node.key:
                if node.left:
                    node = node.left
                else:
                    node.left = self.Node(key, node)
                    self._splay(node.left)
                    return
            else:
                if node.right:
                    node = node.right
                else:
                    node.right = self.Node(key, node)
                    self._splay(node.right)
                    return

    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return  # key not found
        node = self.root  # After search, key is at root if present
        if node.key != key:
            return
        # Remove root
        left = node.left
        right = node.right
        if left:
            left.parent = None
        if right:
            right.parent = None
        if not left:
            self.root = right
        else:
            # Find max in left subtree
            max_left = left
            while max_left.right:
                max_left = max_left.right
            self._splay(max_left)
            # Now, max_left is root of left subtree with no right child
            max_left.right = right
            if right:
                right.parent = max_left
            self.root = max_left

    # Optional: utility methods for debugging and validation
    def _inorder(self, node=None, res=None):
        if res is None:
            res = []
        if node is None:
            node = self.root
        if not node:
            return res
        if node.left:
            self._inorder(node.left, res)
        res.append(node.key)
        if node.right:
            self._inorder(node.right, res)
        return res

    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        return "{" + ", ".join(map(str, self._inorder())) + "}"