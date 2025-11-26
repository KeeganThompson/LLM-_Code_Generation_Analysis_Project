class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # --- Rotation helpers ---
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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    # --- Splaying ---
    def _splay(self, x):
        if not x:
            return
        while x.parent:
            if not x.parent.parent:
                # Zig step
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if g.left == p and p.left == x:
                    # Zig-Zig step (left-left)
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif g.right == p and p.right == x:
                    # Zig-Zig step (right-right)
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif g.left == p and p.right == x:
                    # Zig-Zag step (left-right)
                    self._rotate_left(p)
                    self._rotate_right(g)
                elif g.right == p and p.left == x:
                    # Zig-Zag step (right-left)
                    self._rotate_right(p)
                    self._rotate_left(g)

    # --- Search ---
    def search(self, key):
        node = self.root
        parent = None
        while node:
            if key == node.key:
                self._splay(node)
                return True
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        if parent:
            self._splay(parent)
        return False

    # --- Insert ---
    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return  # Key already in set, do nothing
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

    # --- Delete ---
    def delete(self, key):
        if not self.root:
            return
        # Search and splay the node (or its parent if not found) to root
        node = self.root
        parent = None
        while node:
            if key == node.key:
                self._splay(node)
                break
            parent = node
            if key < node.key:
                node = node.left
            else:
                node = node.right
        else:
            if parent:
                self._splay(parent)
            return  # Key not found, do nothing

        # Now self.root is the node to delete
        if not self.root.left:
            self._replace_root(self.root.right)
        elif not self.root.right:
            self._replace_root(self.root.left)
        else:
            # Both children exist: find maximum in left subtree
            left_sub = self.root.left
            left_sub.parent = None
            max_left = left_sub
            while max_left.right:
                max_left = max_left.right
            # Splay max_left to the root of left_sub
            self._splay_node_in_subtree(max_left, left_sub)
            # Attach right subtree
            max_left.right = self.root.right
            if self.root.right:
                self.root.right.parent = max_left
            self.root = max_left
            self.root.parent = None

    def _replace_root(self, node):
        self.root = node
        if node:
            node.parent = None

    def _splay_node_in_subtree(self, x, subtree_root):
        # Splay x to the root of the subtree rooted at subtree_root
        while x.parent:
            if x.parent == subtree_root:
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
                break
            p = x.parent
            g = p.parent
            if g.left == p and p.left == x:
                self._rotate_right(g)
                self._rotate_right(p)
            elif g.right == p and p.right == x:
                self._rotate_left(g)
                self._rotate_left(p)
            elif g.left == p and p.right == x:
                self._rotate_left(p)
                self._rotate_right(g)
            elif g.right == p and p.left == x:
                self._rotate_right(p)
                self._rotate_left(g)

    # Optional: for debugging or testing
    def to_list(self):
        res = []
        def inorder(node):
            if node:
                inorder(node.left)
                res.append(node.key)
                inorder(node.right)
        inorder(self.root)
        return res