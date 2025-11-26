public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Right rotate
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y != null) {
            x.left = y.right;
            if (y.right != null) y.right.parent = x;
            y.parent = x.parent;
        }
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        if (y != null) y.right = x;
        x.parent = y;
    }

    // Left rotate
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y != null) {
            x.right = y.left;
            if (y.left != null) y.left.parent = x;
            y.parent = x.parent;
        }
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        if (y != null) y.left = x;
        x.parent = y;
    }

    // Splay operation: move x to root
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
    }

    // Public search: splay on found node
    public Integer search(int key) {
        Node x = root;
        Node last = null;
        while (x != null) {
            last = x;
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                splay(x);
                return x.key;
            }
        }
        if (last != null) splay(last);
        return null;
    }

    // Public insert
    public void insert(int key) {
        Node z = root;
        Node p = null;
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                splay(z);
                return; // Key already in set
            }
        }
        Node n = new Node(key);
        n.parent = p;
        if (p == null) {
            root = n;
        } else if (key < p.key) {
            p.left = n;
        } else {
            p.right = n;
        }
        splay(n);
    }

    // Public delete
    public void delete(int key) {
        Node x = root;
        while (x != null) {
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                break;
            }
        }
        if (x == null) return; // Key not found
        splay(x);

        if (x.left == null) {
            replace(x, x.right);
        } else if (x.right == null) {
            replace(x, x.left);
        } else {
            // Both children exist
            Node y = subtreeMin(x.right);
            if (y.parent != x) {
                replace(y, y.right);
                y.right = x.right;
                if (y.right != null) y.right.parent = y;
            }
            replace(x, y);
            y.left = x.left;
            if (y.left != null) y.left.parent = y;
        }
        x.left = x.right = x.parent = null; // Help GC
    }

    // Helper: replace u with v in the tree
    private void replace(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null) v.parent = u.parent;
    }

    // Helper: minimum node in subtree rooted at x
    private Node subtreeMin(Node x) {
        while (x.left != null) x = x.left;
        return x;
    }

    // Optional: For testing/debugging
    // public void inorder() {
    //     inorder(root);
    //     System.out.println();
    // }
    // private void inorder(Node x) {
    //     if (x == null) return;
    //     inorder(x.left);
    //     System.out.print(x.key + " ");
    //     inorder(x.right);
    // }
}