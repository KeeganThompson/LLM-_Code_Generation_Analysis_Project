class SplayTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        # Key lies in left subtree
        if key < root.key:
            if root.left is None:
                return root
            # Zig-Zig (Left Left)
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            # Zig-Zag (Left Right)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            # Second rotation
            return root if root.left is None else self._right_rotate(root)
        else:
            if root.right is None:
                return root
            # Zag-Zig (Right Left)
            if key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            # Zag-Zag (Right Right)
            elif key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            # Second rotation
            return root if root.right is None else self._left_rotate(root)

    def search(self, key):
        """
        Returns True if key is in the set, else False.
        Splays the accessed node (or its parent) to the root.
        """
        self.root = self._splay(self.root, key)
        return self.root is not None and self.root.key == key

    def insert(self, key):
        """
        Inserts key into the set if not present.
        """
        if self.root is None:
            self.root = self.Node(key)
            return

        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return  # Key already in the set

        new_node = self.Node(key)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def delete(self, key):
        """
        Removes key from the set if present.
        """
        if self.root is None:
            return

        self.root = self._splay(self.root, key)
        if self.root.key != key:
            return  # Key not found

        if self.root.left is None:
            self.root = self.root.right
        else:
            temp = self.root.right
            self.root = self._splay(self.root.left, key)
            self.root.right = temp

    # Optional: For debugging/validation
    def __contains__(self, key):
        return self.search(key)

    def __iter__(self):
        # In-order traversal
        stack, node = [], self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key
            node = node.right

    def __repr__(self):
        return "{" + ", ".join(str(k) for k in self) + "}"