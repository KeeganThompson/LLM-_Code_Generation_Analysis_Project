class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # ----------- Splay Operations -----------

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
                # Zig step
                if x.parent.left == x:
                    self._rotate_right(x.parent)
                else:
                    self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.left == x.parent:
                # Zig-zig step
                self._rotate_right(x.parent.parent)
                self._rotate_right(x.parent)
            elif x.parent.right == x and x.parent.parent.right == x.parent:
                # Zig-zig step
                self._rotate_left(x.parent.parent)
                self._rotate_left(x.parent)
            elif x.parent.left == x and x.parent.parent.right == x.parent:
                # Zig-zag step
                self._rotate_right(x.parent)
                self._rotate_left(x.parent)
            else:
                # Zig-zag step
                self._rotate_left(x.parent)
                self._rotate_right(x.parent)

    # ----------- Search Operation -----------

    def search(self, key):
        """
        Returns True if key is present, False otherwise.
        Splays the found node or its parent (if not found) to the root.
        """
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
        # Key not found, splay last accessed node (its parent)
        if last:
            self._splay(last)
        return False

    # ----------- Insert Operation -----------

    def insert(self, key):
        """
        Inserts key into the splay tree. Duplicates are ignored.
        After insertion, the inserted node is splayed to the root.
        """
        if not self.root:
            self.root = self.Node(key)
            return

        x = self.root
        parent = None
        while x:
            parent = x
            if key == x.key:
                self._splay(x)
                return  # Ignore duplicates
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

    # ----------- Delete Operation -----------

    def delete(self, key):
        """
        Removes key from the splay tree if present.
        Splays the deleted node (if found) to the root before deletion.
        """
        if not self.root:
            return

        if not self.search(key):
            return  # Key not found

        # Now self.root.key == key
        node = self.root

        if not node.left:
            self._replace_root(node.right)
        elif not node.right:
            self._replace_root(node.left)
        else:
            # Find maximum in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            # Splay max_left to become new root.left
            self._splay(max_left)
            # Now max_left is root's left child with no right child
            max_left.right = node.right
            if node.right:
                node.right.parent = max_left
            self._replace_root(max_left)

    def _replace_root(self, node):
        self.root = node
        if node:
            node.parent = None

    # ----------- Utility -----------

    # For debugging: in-order traversal as list
    def to_list(self):
        result = []
        def inorder(node):
            if node:
                inorder(node.left)
                result.append(node.key)
                inorder(node.right)
        inorder(self.root)
        return result

# Example usage:
# st = SplayTree()
# st.insert(5)
# st.insert(3)
# st.insert(7)
# print(st.search(3))  # True
# print(st.search(6))  # False
# st.delete(3)
# print(st.to_list())  # [5, 7]