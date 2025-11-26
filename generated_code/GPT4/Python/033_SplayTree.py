class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    def _rotate_left(self, x):
        y = x.right
        if y:
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
        if y:
            y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        if y:
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
        if y:
            y.right = x
        x.parent = y

    def _splay(self, x):
        while x.parent:
            if not x.parent.parent:
                # Zig step
                if x == x.parent.left:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            else:
                p = x.parent
                g = p.parent
                if x == p.left and p == g.left:
                    # Zig-zig step
                    self._rotate_right(g)
                    self._rotate_right(p)
                elif x == p.right and p == g.right:
                    # Zig-zig step
                    self._rotate_left(g)
                    self._rotate_left(p)
                elif x == p.right and p == g.left:
                    # Zig-zag step
                    self._rotate_left(p)
                    self._rotate_right(g)
                elif x == p.left and p == g.right:
                    # Zig-zag step
                    self._rotate_right(p)
                    self._rotate_left(g)

    def search(self, key):
        """Return True if key is found, else False.
        Splay the found node (or last accessed node's parent) to root."""
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
        if prev:
            self._splay(prev)
        return False

    def insert(self, key):
        """Insert key into the splay tree. If already present, do nothing."""
        if not self.root:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
            if key == node.key:
                self._splay(node)
                return  # Already present
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

    def _subtree_maximum(self, node):
        while node.right:
            node = node.right
        return node

    def delete(self, key):
        """Remove key from the splay tree if present."""
        if not self.root:
            return
        # First, search and splay the node (or its parent) to root
        node = self.root
        prev = None
        while node:
            prev = node
            if key == node.key:
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        if node and node.key == key:
            self._splay(node)
        elif prev:
            self._splay(prev)
        else:
            return  # Tree is empty

        # Now the node to be deleted is at root if it exists
        if self.root.key != key:
            return  # Key not found

        if not self.root.left:
            self._replace_root(self.root.right)
        elif not self.root.right:
            self._replace_root(self.root.left)
        else:
            # Both children exist
            left_subtree = self.root.left
            left_subtree.parent = None
            right_subtree = self.root.right
            right_subtree.parent = None
            # Find the max in left subtree
            max_left = self._subtree_maximum(left_subtree)
            self._splay_in_subtree(max_left, left_subtree)
            # max_left is now root of left_subtree, and has no right child
            max_left.right = right_subtree
            if right_subtree:
                right_subtree.parent = max_left
            self.root = max_left

    def _replace_root(self, node):
        if node:
            node.parent = None
        self.root = node

    def _splay_in_subtree(self, x, subtree_root):
        """Splay node x to the root of the provided subtree."""
        while x.parent:
            if not x.parent.parent:
                if x == x.parent.left:
                    self._rotate_right_in_subtree(x.parent, subtree_root)
                else:
                    self._rotate_left_in_subtree(x.parent, subtree_root)
            else:
                p = x.parent
                g = p.parent
                if x == p.left and p == g.left:
                    self._rotate_right_in_subtree(g, subtree_root)
                    self._rotate_right_in_subtree(p, subtree_root)
                elif x == p.right and p == g.right:
                    self._rotate_left_in_subtree(g, subtree_root)
                    self._rotate_left_in_subtree(p, subtree_root)
                elif x == p.right and p == g.left:
                    self._rotate_left_in_subtree(p, subtree_root)
                    self._rotate_right_in_subtree(g, subtree_root)
                elif x == p.left and p == g.right:
                    self._rotate_right_in_subtree(p, subtree_root)
                    self._rotate_left_in_subtree(g, subtree_root)

    def _rotate_left_in_subtree(self, x, subtree_root):
        y = x.right
        if y:
            x.right = y.left
            if y.left:
                y.left.parent = x
            y.parent = x.parent
        if not x.parent:
            # x is root of the subtree
            if x == subtree_root:
                # Update subtree_root pointer in delete
                pass
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        if y:
            y.left = x
        x.parent = y

    def _rotate_right_in_subtree(self, x, subtree_root):
        y = x.left
        if y:
            x.left = y.right
            if y.right:
                y.right.parent = x
            y.parent = x.parent
        if not x.parent:
            if x == subtree_root:
                pass
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        if y:
            y.right = x
        x.parent = y

    # Optional: For debugging, print tree inorder
    def _inorder(self, node):
        if node:
            yield from self._inorder(node.left)
            yield node.key
            yield from self._inorder(node.right)

    def __contains__(self, key):
        return self.search(key)

    def __iter__(self):
        return self._inorder(self.root)

    def __bool__(self):
        return self.root is not None

    def clear(self):
        self.root = None