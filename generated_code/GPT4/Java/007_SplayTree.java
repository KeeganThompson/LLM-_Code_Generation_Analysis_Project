public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Public insert method
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node z = root;
        Node p = null;
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                // Duplicate key, splay the existing node
                splay(z);
                return;
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

    // Public delete method
    public void delete(int key) {
        Node n = find(root, key);
        if (n == null)
            return;
        splay(n);

        if (n.left == null) {
            replace(n, n.right);
        } else if (n.right == null) {
            replace(n, n.left);
        } else {
            Node min = subtreeMin(n.right);
            if (min.parent != n) {
                replace(min, min.right);
                min.right = n.right;
                if (min.right != null)
                    min.right.parent = min;
            }
            replace(n, min);
            min.left = n.left;
            if (min.left != null)
                min.left.parent = min;
        }
        n.left = n.right = n.parent = null; // Help GC
    }

    // Public search method
    public Integer search(int key) {
        Node n = find(root, key);
        if (n != null) {
            splay(n);
            return n.key;
        }
        return null;
    }

    // Helper: Find node with key in subtree rooted at n
    private Node find(Node n, int key) {
        while (n != null) {
            if (key < n.key)
                n = n.left;
            else if (key > n.key)
                n = n.right;
            else
                return n;
        }
        return null;
    }

    // Splay the node x to the root
    private void splay(Node x) {
        if (x == null)
            return;

        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x == x.parent.left)
                    rotateRight(x.parent);
                else
                    rotateLeft(x.parent);
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-Zig
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-Zig
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-Zag
                rotateLeft(x.parent);
                rotateRight(x.parent);
            } else {
                // Zig-Zag
                rotateRight(x.parent);
                rotateLeft(x.parent);
            }
        }
        root = x;
    }

    // Rotate left at node x
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;

        x.right = y.left;
        if (y.left != null)
            y.left.parent = x;
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

    // Rotate right at node x
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;

        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.right = x;
        x.parent = y;
    }

    // Replace node u with node v in the tree
    private void replace(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null)
            v.parent = u.parent;
    }

    // Find subtree minimum
    private Node subtreeMin(Node x) {
        while (x.left != null)
            x = x.left;
        return x;
    }

    // For debugging: In-order traversal
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