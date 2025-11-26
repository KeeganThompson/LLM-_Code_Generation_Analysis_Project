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

    # ---------- Helper Methods ----------

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
            g = p.parent
            if not g:
                # Zig
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            else:
                if x == p.left and p == g.left:
                    # Zig-Zig
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif x == p.right and p == g.right:
                    # Zig-Zig
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif x == p.right and p == g.left:
                    # Zig-Zag
                    self._rotate_left(p)
                    self._rotate_right(g)
                else: # x == p.left and p == g.right
                    # Zig-Zag
                    self._rotate_right(p)
                    self._rotate_left(g)

    def _subtree_minimum(self, x):
        while x.left:
            x = x.left
        return x

    def _subtree_maximum(self, x):
        while x.right:
            x = x.right
        return x

    # ---------- Public Methods ----------

    def insert(self, key):
        """Insert key into the splay tree."""
        if not self.root:
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
                # Key already present, splay to root
                self._splay(parent)
                return

        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def search(self, key):
        """
        Search for key in the splay tree.
        If found, splay the node to root and return True.
        If not found, splay the last accessed node (closest ancestor) to root and return False.
        """
        x = self.root
        last = None
        while x:
            last = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self._splay(x)
                return True
        if last:
            self._splay(last)
        return False

    def delete(self, key):
        """
        Remove key from the splay tree.
        Splays the node to be deleted (if found) to the root before deletion.
        """
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found

        # Now, self.root.key == key
        root = self.root
        if not root.left:
            self.root = root.right
            if self.root:
                self.root.parent = None
        elif not root.right:
            self.root = root.left
            if self.root:
                self.root.parent = None
        else:
            # Both children exist
            left_subtree = root.left
            left_subtree.parent = None
            right_subtree = root.right
            right_subtree.parent = None

            # Find max in left subtree
            max_left = self._subtree_maximum(left_subtree)
            self._splay(max_left)
            # After splaying, max_left is root of left_subtree, has no right child
            max_left.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_left
            self.root = max_left

    # ---------- Optional: Utility for testing ----------

    def _inorder(self, x, res):
        if x:
            self._inorder(x.left, res)
            res.append(x.key)
            self._inorder(x.right, res)

    def to_list(self):
        """Return inorder list of keys."""
        res = []
        self._inorder(self.root, res)
        return res

# Example usage:
# s = SplayTree()
# s.insert(5)
# s.insert(3)
# s.insert(9)
# print(s.search(3)) # True
# s.delete(5)
# print(s.to_list()) # [3,9]