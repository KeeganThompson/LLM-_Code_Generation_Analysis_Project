public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key, Node parent) {
            this.key = key;
            this.parent = parent;
        }
    }

    private Node root;

    /**
     * Inserts the key into the splay tree. If the key already exists, does nothing.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
            return;
        }

        Node curr = root;
        Node parent = null;
        while (curr != null) {
            parent = curr;
            if (key < curr.key) {
                curr = curr.left;
            } else if (key > curr.key) {
                curr = curr.right;
            } else {
                // Key already exists; splay it to root
                splay(curr);
                return;
            }
        }

        Node newNode = new Node(key, parent);
        if (key < parent.key)
            parent.left = newNode;
        else
            parent.right = newNode;

        splay(newNode);
    }

    /**
     * Deletes the key from the splay tree. If the key does not exist, does nothing.
     */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return;

        splay(node);
        if (node.left == null) {
            replace(node, node.right);
        } else if (node.right == null) {
            replace(node, node.left);
        } else {
            Node min = subtreeMin(node.right);
            if (min.parent != node) {
                replace(min, min.right);
                min.right = node.right;
                if (min.right != null)
                    min.right.parent = min;
            }
            replace(node, min);
            min.left = node.left;
            if (min.left != null)
                min.left.parent = min;
        }
        node.left = node.right = node.parent = null;
    }

    /**
     * Searches for the key in the splay tree.
     * If found, splays the node to the root and returns the key.
     * If not found, splay the last accessed node and returns null.
     */
    public Integer search(int key) {
        Node curr = root;
        Node last = null;
        while (curr != null) {
            last = curr;
            if (key == curr.key) {
                splay(curr);
                return curr.key;
            }
            if (key < curr.key)
                curr = curr.left;
            else
                curr = curr.right;
        }
        if (last != null)
            splay(last);
        return null;
    }

    // Helper methods

    private Node findNode(int key) {
        Node curr = root;
        while (curr != null) {
            if (key == curr.key)
                return curr;
            if (key < curr.key)
                curr = curr.left;
            else
                curr = curr.right;
        }
        return null;
    }

    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig step
                if (x == p.left)
                    rotateRight(p);
                else
                    rotateLeft(p);
            } else if (x == p.left && p == g.left) {
                // Zig-Zig step
                rotateRight(g);
                rotateRight(p);
            } else if (x == p.right && p == g.right) {
                // Zig-Zig step
                rotateLeft(g);
                rotateLeft(p);
            } else if (x == p.right && p == g.left) {
                // Zig-Zag step
                rotateLeft(p);
                rotateRight(g);
            } else if (x == p.left && p == g.right) {
                // Zig-Zag step
                rotateRight(p);
                rotateLeft(g);
            }
        }
        root = x;
    }

    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null)
            y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.right = x;
        x.parent = y;
    }

    private void replace(Node u, Node v) {
        if (u.parent == null)
            root = v;
        else if (u == u.parent.left)
            u.parent.left = v;
        else
            u.parent.right = v;
        if (v != null)
            v.parent = u.parent;
    }

    private Node subtreeMin(Node node) {
        while (node.left != null)
            node = node.left;
        return node;
    }
}