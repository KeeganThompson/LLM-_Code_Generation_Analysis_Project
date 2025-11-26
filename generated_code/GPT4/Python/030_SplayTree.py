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

    # Right rotation
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

    # Left rotation
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

    # Splay node x to root
    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-zig
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-zig
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            else:
                # Zig-zag
                if x.parent.left == x and x.parent.parent.right == x.parent:
                    self._rotate_right(x.parent)
                    self._rotate_left(x.parent)
                else:
                    self._rotate_left(x.parent)
                    self._rotate_right(x.parent)

    # Search for a key and splay accessed node (or its parent if not found)
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
        # Splay last accessed node (parent of where key would be)
        if last:
            self._splay(last)
        return False

    # Insert a key (no duplicates)
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
                return  # Key already present
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

    # Find the node with a given key
    def _find(self, key):
        node = self.root
        while node:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    # Replace u in parent with v
    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Find maximum node in subtree
    def _subtree_max(self, node):
        while node.right:
            node = node.right
        return node

    # Delete a key
    def delete(self, key):
        node = self._find(key)
        if not node:
            # Splay last accessed node if key not found
            self.search(key)
            return
        self._splay(node)
        # Now node is at root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Both children present
            # Find predecessor (max in left subtree)
            max_left = self._subtree_max(node.left)
            if max_left.parent != node:
                self._replace(max_left, max_left.left)
                max_left.left = node.left
                max_left.left.parent = max_left
            self._replace(node, max_left)
            max_left.right = node.right
            if max_left.right:
                max_left.right.parent = max_left
            max_left.parent = None
            self.root = max_left
        # Node is removed

    # For debugging: inorder traversal
    def inorder(self):
        def _inorder(node):
            if not node:
                return []
            return _inorder(node.left) + [node.key] + _inorder(node.right)
        return _inorder(self.root)