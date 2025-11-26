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

    # ----------- Rotation helpers -----------
    def _rotate_left(self, x):
        y = x.right
        if y is None:
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
        if y is None:
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

    # ----------- Splaying -----------
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            if not x.parent.parent:
                # Zig
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x == x.parent.left and x.parent == x.parent.parent.left:
                # Zig-Zig
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.right:
                # Zig-Zig
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x == x.parent.right and x.parent == x.parent.parent.left:
                # Zig-Zag
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)
            else:
                # Zig-Zag
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)

    # ----------- Search (with splay) -----------
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
        # Not found: splay the last accessed node (prev) to root
        if prev:
            self._splay(prev)
        return False

    # ----------- Insert -----------
    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                # No duplicates in set
                self._splay(node)
                return
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

    # ----------- Delete -----------
    def delete(self, key):
        if not self.root:
            return
        node = self.root
        while node:
            if key == node.key:
                self._splay(node)
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        else:
            # Not found: splay last accessed (None or leaf) node's parent to root
            return  # Key not found, do nothing

        # Now node is at root
        if not node.left:
            self._replace_root_with(node.right)
        elif not node.right:
            self._replace_root_with(node.left)
        else:
            # Both children exist
            # Find max in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            # Splay max_left to the root of the left subtree
            self._splay(max_left)
            # Now max_left is root of left subtree, attach right subtree
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self._replace_root_with(max_left)

    def _replace_root_with(self, node):
        if node:
            node.parent = None
        self.root = node

    # ----------- For debugging / printing -----------
    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        lines = []
        def _print(node, prefix=""):
            if node is not None:
                _print(node.right, prefix + "   ")
                lines.append(prefix + str(node.key))
                _print(node.left, prefix + "   ")
        _print(self.root)
        return "\n".join(lines)

# Example usage:
# tree = SplayTree()
# tree.insert(10)
# tree.insert(20)
# tree.insert(5)
# print(tree)
# print(tree.search(10))
# tree.delete(10)
# print(tree)