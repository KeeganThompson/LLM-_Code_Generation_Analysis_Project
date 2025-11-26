class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Rotate node x to the left
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
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    # Rotate node x to the right
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
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.right = x
        x.parent = y

    # Splay the node x to the root
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
                    # Zig-zig (left-left)
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif p.right == x and g.right == p:
                    # Zig-zig (right-right)
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif p.left == x and g.right == p:
                    # Zig-zag (left-right)
                    self._rotate_right(p)
                    self._rotate_left(g)
                else:
                    # Zig-zag (right-left)
                    self._rotate_left(p)
                    self._rotate_right(g)

    # Insert key into the tree
    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                self._splay(node)
                return  # Already exists
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    # Search for key and splay accessed node or its parent if not found
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
        # Not found; splay the last accessed node (prev) if exists
        if prev:
            self._splay(prev)
        return False

    # Find node with given key
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

    # Replace node u with node v in parent
    def _replace(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Find maximum node in subtree rooted at node
    def _subtree_max(self, node):
        while node.right:
            node = node.right
        return node

    # Delete key from the tree
    def delete(self, key):
        node = self._find(key)
        if not node:
            # Splay last accessed node (for splay set, not strictly necessary)
            self.search(key)
            return
        self._splay(node)
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Both children exist
            # Find max in left subtree
            y = self._subtree_max(node.left)
            if y.parent != node:
                self._replace(y, y.left)
                y.left = node.left
                y.left.parent = y
            self._replace(node, y)
            y.right = node.right
            y.right.parent = y
        # After deletion, the root is at the place where the deleted node was

    # For debugging: Inorder traversal
    def inorder(self):
        def _inorder(node):
            if not node:
                return []
            return _inorder(node.left) + [node.key] + _inorder(node.right)
        return _inorder(self.root)