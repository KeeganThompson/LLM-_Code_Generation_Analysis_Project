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
                # Zig
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if p.left == x and g.left == p:
                    # Zig-zig
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif p.right == x and g.right == p:
                    # Zig-zig
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif p.left == x and g.right == p:
                    # Zig-zag
                    self._rotate_right(p)
                    self._rotate_left(g)
                else:
                    # Zig-zag
                    self._rotate_left(p)
                    self._rotate_right(g)

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
        # Splay the last accessed node (parent of where the key would be)
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return True
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return False  # Key already exists, no insertion
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
        return True

    def _subtree_minimum(self, node):
        while node.left:
            node = node.left
        return node

    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    def delete(self, key):
        node = self.root
        while node:
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        if not node:
            # Splay the last accessed node (parent of where the key would be)
            # For uniformity, let's splay the last accessed parent
            return False  # Key not found
        self._splay(node)
        # After splaying, node is at root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Both children exist
            # Find min in right subtree
            min_right = self._subtree_minimum(node.right)
            if min_right.parent != node:
                self._replace(min_right, min_right.right)
                min_right.right = node.right
                min_right.right.parent = min_right
            self._replace(node, min_right)
            min_right.left = node.left
            min_right.left.parent = min_right
        return True

    # Optional: For testing and visualization
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)
    def to_list(self):
        res = []
        self._inorder(self.root, res)
        return res

# Example usage:
# s = SplayTree()
# s.insert(10)
# s.insert(20)
# s.insert(5)
# print(s.to_list())   # [5, 10, 20]
# print(s.search(20))  # True
# print(s.root.key)    # 20
# s.delete(10)
# print(s.to_list())   # [5, 20]