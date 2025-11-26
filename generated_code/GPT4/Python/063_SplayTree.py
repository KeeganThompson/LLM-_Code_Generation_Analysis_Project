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
        else:  # Key lies in right subtree
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

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return

        # Splay the closest to root
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return  # Already in tree, do nothing

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
        if self.root is None:
            return

        self.root = self._splay(self.root, key)
        if self.root.key != key:
            return  # Not found

        # Now root.key == key
        if self.root.left is None:
            self.root = self.root.right
        else:
            # Splay the largest node in left subtree to root
            l = self.root.left
            l = self._splay(l, key)
            # Find maximum in left subtree
            max_node = l
            while max_node.right:
                max_node = max_node.right
            l = self._splay(l, max_node.key)
            l.right = self.root.right
            self.root = l

    def search(self, key):
        if self.root is None:
            return False
        self.root = self._splay(self.root, key)
        return self.root.key == key

    # Optional: for debugging
    def _inorder(self, node, res):
        if node:
            self._inorder(node.left, res)
            res.append(node.key)
            self._inorder(node.right, res)

    def to_list(self):
        res = []
        self._inorder(self.root, res)
        return res