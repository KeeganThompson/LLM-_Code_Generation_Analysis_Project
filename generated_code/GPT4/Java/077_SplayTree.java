public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;
        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    /** Inserts key into the set. Does nothing if key already exists. */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node z = root, p = null;
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                splay(z);
                return; // already exists
            }
        }
        Node n = new Node(key);
        n.parent = p;
        if (key < p.key) {
            p.left = n;
        } else {
            p.right = n;
        }
        splay(n);
    }

    /** Deletes key from the set. Does nothing if key is not found. */
    public void delete(int key) {
        Node n = findNode(key);
        if (n == null) return;
        splay(n);
        if (n.left == null) {
            transplant(n, n.right);
        } else if (n.right == null) {
            transplant(n, n.left);
        } else {
            Node y = subtreeMin(n.right);
            if (y.parent != n) {
                transplant(y, y.right);
                y.right = n.right;
                if (y.right != null) y.right.parent = y;
            }
            transplant(n, y);
            y.left = n.left;
            if (y.left != null) y.left.parent = y;
        }
        // Remove references for GC
        n.left = n.right = n.parent = null;
    }

    /** Searches for key, splays it to root if found, returns key or null. */
    public Integer search(int key) {
        Node n = findNode(key);
        if (n != null) {
            splay(n);
            return n.key;
        }
        return null;
    }

    // --- Helper Methods ---

    private Node findNode(int key) {
        Node z = root;
        while (z != null) {
            if (key < z.key)
                z = z.left;
            else if (key > z.key)
                z = z.right;
            else
                return z;
        }
        return null;
    }

    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-Zig
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-Zig
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-Zag
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-Zag
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
        root = x;
    }

    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }

    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        y.right = x;
        x.parent = y;
    }

    private void transplant(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null) v.parent = u.parent;
    }

    private Node subtreeMin(Node n) {
        while (n.left != null) n = n.left;
        return n;
    }

    // Optional: For testing
    /*
    public void printInOrder() {
        printInOrder(root);
        System.out.println();
    }

    private void printInOrder(Node n) {
        if (n == null) return;
        printInOrder(n.left);
        System.out.print(n.key + " ");
        printInOrder(n.right);
    }
    */
}