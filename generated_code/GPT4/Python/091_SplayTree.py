class SplayTree:
    class Node:
        __slots__ = ('key', 'left', 'right', 'parent')

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
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:
                # Zig
                if x == p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)
            elif x == p.left and p == gp.left:
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
            else:
                # x == p.left and p == gp.right
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
        if not self.root:
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
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def _subtree_min(self, node):
        while node.left:
            node = node.left
        return node

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
            # Node not found; splay the last accessed node (or its parent)
            if node is None and self.root:
                # last = parent of where the key would be
                # Already at root
                return
            return
        # Node is at root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            min_right = self._subtree_min(node.right)
            if min_right.parent != node:
                self._replace(min_right, min_right.right)
                min_right.right = node.right
                if min_right.right:
                    min_right.right.parent = min_right
            self._replace(node, min_right)
            min_right.left = node.left
            if min_right.left:
                min_right.left.parent = min_right
        del node

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
    def inorder(self):
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return result

# Example Usage:
if __name__ == "__main__":
    st = SplayTree()
    st.insert(5)
    st.insert(3)
    st.insert(8)
    st.insert(7)
    st.insert(10)
    print("Inorder after inserts:", st.inorder())  # Should print [3, 5, 7, 8, 10]
    print("Search 7:", st.search(7))  # Should splay 7 to root
    print("Root after searching 7:", st.root.key)
    st.delete(5)
    print("Inorder after deleting 5:", st.inorder())  # Should print [3, 7, 8, 10]
    print("Search 100:", st.search(100))  # Not found, splay last accessed node
    print("Root after searching 100 (not found):", st.root.key)