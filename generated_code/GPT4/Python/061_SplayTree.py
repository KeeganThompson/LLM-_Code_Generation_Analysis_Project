class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Rotate node x up
    def _rotate(self, x):
        p = x.parent
        if not p:
            return  # x is root
        g = p.parent
        if p.left == x:
            # Right rotation
            p.left = x.right
            if x.right:
                x.right.parent = p
            x.right = p
        else:
            # Left rotation
            p.right = x.left
            if x.left:
                x.left.parent = p
            x.left = p
        p.parent = x
        x.parent = g
        if g:
            if g.left == p:
                g.left = x
            else:
                g.right = x
        else:
            self.root = x

    # Splay node x to root
    def _splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                # Zig step
                self._rotate(x)
            elif (g.left == p and p.left == x) or (g.right == p and p.right == x):
                # Zig-zig step
                self._rotate(p)
                self._rotate(x)
            else:
                # Zig-zag step
                self._rotate(x)
                self._rotate(x)

    # Find node with key, splay last accessed node (found or last parent) to root
    def search(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key == x.key:
                self._splay(x)
                return True
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        x = self.root
        parent = None
        while x:
            parent = x
            if key == x.key:
                self._splay(x)  # Splay existing node
                return
            elif key < x.key:
                x = x.left
            else:
                x = x.right
        new_node = self.Node(key, parent)
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def delete(self, key):
        if not self.root:
            return
        if not self.search(key):
            return  # Key not found, root is closest node after splay
        # Now root.key == key
        node = self.root
        if not node.left:
            self.root = node.right
            if self.root:
                self.root.parent = None
        elif not node.right:
            self.root = node.left
            if self.root:
                self.root.parent = None
        else:
            # Find max in left subtree
            left_subtree = node.left
            left_subtree.parent = None
            max_left = left_subtree
            while max_left.right:
                max_left = max_left.right
            # Splay the max node of the left subtree
            self._splay(max_left)
            # Now max_left is root of left subtree
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self.root = max_left
            max_left.parent = None

    # For debugging: Inorder traversal as sorted list
    def to_list(self):
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        inorder(self.root)
        return result