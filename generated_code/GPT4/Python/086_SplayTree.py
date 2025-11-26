class SplayTree:
    class Node:
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
        if x.parent is None:
            self.root = y
        else:
            if x == x.parent.left:
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
        if x.parent is None:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    # Splaying operation
    def _splay(self, x):
        if x is None:
            return
        while x.parent:
            if x.parent.parent is None:
                # Zig step
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if p.left == x and g.left == p:
                    # Zig-zig step (left-left)
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif p.right == x and g.right == p:
                    # Zig-zig step (right-right)
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif p.left == x and g.right == p:
                    # Zig-zag step (left-right)
                    self._rotate_right(p)
                    self._rotate_left(g)
                else:
                    # Zig-zag step (right-left)
                    self._rotate_left(p)
                    self._rotate_right(g)

    # Internal search, returns (node, found)
    def _find(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                return x, True
        return last, False

    def search(self, key):
        """Search for key and splay the accessed node (or its parent if not found) to the root.
        Returns True if key found, else False."""
        node, found = self._find(key)
        if node is not None:
            self._splay(node)
        return found

    def insert(self, key):
        """Insert key into the splay tree."""
        if self.root is None:
            self.root = self.Node(key)
            return
        node, found = self._find(key)
        self._splay(node)
        if found:
            # Key already exists, no duplicates in set
            return
        # Insert new node
        new_node = self.Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            if self.root.left:
                self.root.left.parent = new_node
            self.root.left = None
            self.root.parent = new_node
            new_node.parent = None
            self.root = new_node
        else:  # key > self.root.key
            new_node.left = self.root
            new_node.right = self.root.right
            if self.root.right:
                self.root.right.parent = new_node
            self.root.right = None
            self.root.parent = new_node
            new_node.parent = None
            self.root = new_node

    def delete(self, key):
        """Delete key from the splay tree."""
        node, found = self._find(key)
        if not found:
            if node:
                self._splay(node)
            return  # Key not found
        self._splay(node)
        # Now node is at root
        if self.root.left is None:
            self._replace_root(self.root.right)
        elif self.root.right is None:
            self._replace_root(self.root.left)
        else:
            # Save right subtree
            right = self.root.right
            right.parent = None
            # Find max in left subtree
            left = self.root.left
            left.parent = None
            max_left = left
            while max_left.right:
                max_left = max_left.right
            self._splay(max_left)
            # Now max_left is root of left subtree and has no right child
            self.root.right = right
            if right:
                right.parent = self.root

    def _replace_root(self, node):
        if node:
            node.parent = None
        self.root = node

    # For debugging: in-order traversal
    def inorder(self):
        result = []
        def _inorder(x):
            if x:
                _inorder(x.left)
                result.append(x.key)
                _inorder(x.right)
        _inorder(self.root)
        return result