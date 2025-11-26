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

    # Right rotation
    def _right_rotate(self, x):
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
    def _left_rotate(self, x):
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
                # Zig
                if x == x.parent.left:
                    self._right_rotate(x.parent)
                else:
                    self._left_rotate(x.parent)
            else:
                if x == x.parent.left and x.parent == x.parent.parent.left:
                    # Zig-Zig
                    self._right_rotate(x.parent.parent)
                    self._right_rotate(x.parent)
                elif x == x.parent.right and x.parent == x.parent.parent.right:
                    # Zig-Zig
                    self._left_rotate(x.parent.parent)
                    self._left_rotate(x.parent)
                elif x == x.parent.right and x.parent == x.parent.parent.left:
                    # Zig-Zag
                    self._left_rotate(x.parent)
                    self._right_rotate(x.parent)
                elif x == x.parent.left and x.parent == x.parent.parent.right:
                    # Zig-Zag
                    self._right_rotate(x.parent)
                    self._left_rotate(x.parent)

    # Search operation with splaying
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
        # Splay the last accessed parent if not found
        if last:
            self._splay(last)
        return False

    # Insert operation
    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return

        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return  # No duplicates
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

    # Find node with key
    def _find(self, key):
        node = self.root
        last = None
        while node:
            last = node
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return last

    # Join two subtrees
    def _join(self, left, right):
        if not left:
            return right
        if not right:
            return left
        # Find max in left
        node = left
        while node.right:
            node = node.right
        self._splay(node)
        node.right = right
        if right:
            right.parent = node
        return node

    # Delete operation
    def delete(self, key):
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
            # Not found, splay the last accessed node
            last = self._find(key)
            if last:
                self._splay(last)
            return  # Key not found

        # Now node is root
        left = node.left
        right = node.right
        if left:
            left.parent = None
        if right:
            right.parent = None
        self.root = self._join(left, right)

    # For debug: inorder traversal
    def inorder(self):
        result = []
        def _inorder(node):
            if node:
                _inorder(node.left)
                result.append(node.key)
                _inorder(node.right)
        _inorder(self.root)
        return result

    # For debug: check if a key exists
    def __contains__(self, key):
        return self.search(key)