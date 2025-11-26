class SplayTree:
    class Node:
        def __init__(self, key):
            self.key = key
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        self.root = None

    def _rotate(self, x):
        p = x.parent
        if p is None:
            return
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

    def _splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent
            if not g:
                # Zig
                self._rotate(x)
            elif (g.left == p and p.left == x) or (g.right == p and p.right == x):
                # Zig-zig
                self._rotate(p)
                self._rotate(x)
            else:
                # Zig-zag
                self._rotate(x)
                self._rotate(x)

    def search(self, key):
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
                self._splay(node)
                return True
        if last:
            self._splay(last)
        return False

    def insert(self, key):
        if self.root is None:
            self.root = self.Node(key)
            return
        node = self.root
        parent = None
        while node:
            parent = node
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
                self._splay(node)
                return  # Already in tree
        new_node = self.Node(key)
        new_node.parent = parent
        if key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node
        self._splay(new_node)

    def delete(self, key):
        if not self.search(key):
            return  # Not found; nothing to delete
        node = self.root
        # Now node.key == key and node is at root
        if not node.left:
            self._replace(node, node.right)
        elif not node.right:
            self._replace(node, node.left)
        else:
            # Find max in left subtree
            max_left = node.left
            while max_left.right:
                max_left = max_left.right
            if max_left.parent != node:
                self._replace(max_left, max_left.left)
                max_left.left = node.left
                if max_left.left:
                    max_left.left.parent = max_left
            self._replace(node, max_left)
            max_left.right = node.right
            if max_left.right:
                max_left.right.parent = max_left

    def _replace(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v:
            v.parent = u.parent

    # Optional: For debugging purpose only
    def __contains__(self, key):
        return self.search(key)

    def __str__(self):
        # Breadth-first traversal
        if not self.root:
            return "<empty>"
        result = []
        queue = [(self.root, 0)]
        curr_level = 0
        level_nodes = []
        while queue:
            node, level = queue.pop(0)
            if level != curr_level:
                result.append(" ".join(str(n) for n in level_nodes))
                level_nodes = []
                curr_level = level
            if node:
                level_nodes.append(node.key)
                queue.append((node.left, level+1))
                queue.append((node.right, level+1))
            else:
                level_nodes.append("N")
        result.append(" ".join(str(n) for n in level_nodes))
        return "\n".join(result)