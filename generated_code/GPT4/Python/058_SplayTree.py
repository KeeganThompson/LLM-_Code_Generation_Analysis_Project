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

    def _splay(self, x):
        while x.parent:
            if x.parent.parent is None:
                # Zig
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                if x == x.parent.left and x.parent == x.parent.parent.left:
                    # Zig-Zig (left left)
                    self._rotate_right(x.parent.parent)
                    self._rotate_right(x.parent)
                elif x == x.parent.right and x.parent == x.parent.parent.right:
                    # Zig-Zig (right right)
                    self._rotate_left(x.parent.parent)
                    self._rotate_left(x.parent)
                elif x == x.parent.right and x.parent == x.parent.parent.left:
                    # Zig-Zag (left right)
                    self._rotate_left(x.parent)
                    self._rotate_right(x.parent)
                else:
                    # Zig-Zag (right left)
                    self._rotate_right(x.parent)
                    self._rotate_left(x.parent)

    def search(self, key):
        """
        Returns True if key exists in the set, else False.
        After search, the accessed node (found or last accessed) is splayed to root.
        """
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

    def insert(self, key):
        """
        Inserts key into the set if not already present.
        """
        if not self.root:
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

    def _subtree_minimum(self, x):
        while x.left:
            x = x.left
        return x

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        else:
            if u == u.parent.left:
                u.parent.left = v
            else:
                u.parent.right = v
        if v:
            v.parent = u.parent

    def delete(self, key):
        """
        Deletes key from the set if present.
        """
        x = self.root
        while x:
            if key == x.key:
                self._splay(x)
                break
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        else:
            # Not found, splay last accessed node if any
            if self.root:
                # Find closest
                self.search(key)
            return  # Key not found

        # Now x is at root
        if x.left is None:
            self._replace(x, x.right)
        elif x.right is None:
            self._replace(x, x.left)
        else:
            # Find min in right subtree
            y = self._subtree_minimum(x.right)
            if y.parent != x:
                self._replace(y, y.right)
                y.right = x.right
                y.right.parent = y
            self._replace(x, y)
            y.left = x.left
            y.left.parent = y
        # No need to splay after deletion

    # Optional: for debugging and testing
    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        def print_tree(node, indent=""):
            if not node:
                return ""
            result = ""
            result += print_tree(node.right, indent + "   ")
            result += f"{indent}{node.key}\n"
            result += print_tree(node.left, indent + "   ")
            return result
        return print_tree(self.root)