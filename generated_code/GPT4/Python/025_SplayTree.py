class SplayTree:
    class Node:
        def __init__(self, key, parent=None):
            self.key = key
            self.left = None
            self.right = None
            self.parent = parent

    def __init__(self):
        self.root = None

    # Rotate node x with its parent
    def _rotate(self, x):
        p = x.parent
        if not p:
            return
        gp = p.parent
        if p.left == x:
            b = x.right
            x.right = p
            p.left = b
            if b:
                b.parent = p
        else:
            b = x.left
            x.left = p
            p.right = b
            if b:
                b.parent = p
        x.parent = gp
        p.parent = x
        if gp:
            if gp.left == p:
                gp.left = x
            else:
                gp.right = x
        else:
            self.root = x

    # Splay operation: move x to root
    def _splay(self, x):
        while x.parent:
            p = x.parent
            gp = p.parent
            if not gp:
                # Zig
                self._rotate(x)
            elif (gp.left == p and p.left == x) or (gp.right == p and p.right == x):
                # Zig-zig
                self._rotate(p)
                self._rotate(x)
            else:
                # Zig-zag
                self._rotate(x)
                self._rotate(x)

    # Find node with key, or last accessed node (parent if not found)
    def _find(self, key):
        node = self.root
        last = None
        while node:
            last = node
            if key < node.key:
                if node.left:
                    node = node.left
                else:
                    break
            elif key > node.key:
                if node.right:
                    node = node.right
                else:
                    break
            else:
                break
        return node, last

    # Public search: splay the found node or last accessed node (parent if not found)
    def search(self, key):
        node, last = self._find(key)
        if node and node.key == key:
            self._splay(node)
            return True
        elif last:
            self._splay(last)
            return False
        else:
            return False

    # Public insert
    def insert(self, key):
        if not self.root:
            self.root = self.Node(key)
            return
        node, last = self._find(key)
        if node and node.key == key:
            self._splay(node)
            return  # Already exists
        new_node = self.Node(key)
        if key < last.key:
            last.left = new_node
            new_node.parent = last
        else:
            last.right = new_node
            new_node.parent = last
        self._splay(new_node)

    # Find maximum node in subtree
    def _subtree_max(self, node):
        while node.right:
            node = node.right
        return node

    # Public delete
    def delete(self, key):
        node, last = self._find(key)
        if not node or node.key != key:
            if last:
                self._splay(last)
            return  # Not found

        self._splay(node)  # Splay the node to root
        left_sub = node.left
        right_sub = node.right

        if left_sub:
            left_sub.parent = None
        if right_sub:
            right_sub.parent = None

        if not left_sub:
            self.root = right_sub
        else:
            max_left = self._subtree_max(left_sub)
            self._splay(max_left)
            max_left.right = right_sub
            if right_sub:
                right_sub.parent = max_left
            self.root = max_left

    # For testing and visualization (not required by prompt)
    def inorder(self):
        result = []
        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            result.append(node.key)
            _inorder(node.right)
        _inorder(self.root)
        return result