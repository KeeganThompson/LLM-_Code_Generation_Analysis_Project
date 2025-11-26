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
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        if not x:
            return
        while x.parent:
            if not x.parent.parent:
                # Zig case
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if x == p.left and p == g.left:
                    # Zig-zig case (left-left)
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif x == p.right and p == g.right:
                    # Zig-zig case (right-right)
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif x == p.right and p == g.left:
                    # Zig-zag case (left-right)
                    self._rotate_left(p)
                    self._rotate_right(g)
                elif x == p.left and p == g.right:
                    # Zig-zag case (right-left)
                    self._rotate_right(p)
                    self._rotate_left(g)

    def search(self, key):
        """
        Returns True if key is present, else False.
        Splays the accessed node or its parent (if not found) to root.
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

    def insert(self, key):
        """
        Inserts key into the splay tree. If already present, does nothing.
        After insertion, the inserted node is splayed to the root.
        """
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
                self._splay(x)
                return  # Key already in set

        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._splay(new_node)

    def _subtree_minimum(self, x):
        while x.left:
            x = x.left
        return x

    def delete(self, key):
        """
        Deletes key from the splay tree. If not present, does nothing.
        After deletion, splay the parent of the deleted node (or last accessed node) to root.
        """
        node = self.root
        parent = None
        while node:
            if key < node.key:
                parent = node
                node = node.left
            elif key > node.key:
                parent = node
                node = node.right
            else:
                self._splay(node)
                # Now node is root
                if not node.left:
                    self._replace(node, node.right)
                elif not node.right:
                    self._replace(node, node.left)
                else:
                    min_right = self._subtree_minimum(node.right)
                    if min_right.parent != node:
                        self._replace(min_right, min_right.right)
                        min_right.right = node.right
                        if min_right.right:
                            min_right.right.parent = min_right
                    self._replace(node, min_right)
                    min_right.left = node.left
                    if min_right.left:
                        min_right.left.parent = min_right
                return  # Deleted
        if parent:
            self._splay(parent)  # Splay last accessed parent to root

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: For debugging and testing
    def in_order(self):
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        inorder(self.root)
        return result