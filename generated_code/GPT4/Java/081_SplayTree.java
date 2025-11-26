public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;
        Node(int key) { this.key = key; }
    }

    private Node root;

    // Public method to insert a key
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
                // Key already exists, splay it
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

    // Public method to delete a key
    public void delete(int key) {
        Node node = find(key);
        if (node == null) return;

        splay(node);

        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            // Now maxLeft is root, and it has no right child
            maxLeft.right = node.right;
            if (node.right != null) node.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
    }

    // Public method to search for a key and splay it to root
    public Integer search(int key) {
        Node node = find(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with key
    private Node find(int key) {
        Node z = root;
        while (z != null) {
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                return z;
            }
        }
        return null;
    }

    // Helper: Splay the node to root
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

    // Helper: Right rotation
    private void rotateRight(Node p) {
        Node x = p.left;
        if (x == null) return;
        p.left = x.right;
        if (x.right != null) x.right.parent = p;
        x.parent = p.parent;
        if (p.parent == null) {
            root = x;
        } else if (p.parent.left == p) {
            p.parent.left = x;
        } else {
            p.parent.right = x;
        }
        x.right = p;
        p.parent = x;
    }

    // Helper: Left rotation
    private void rotateLeft(Node p) {
        Node x = p.right;
        if (x == null) return;
        p.right = x.left;
        if (x.left != null) x.left.parent = p;
        x.parent = p.parent;
        if (p.parent == null) {
            root = x;
        } else if (p.parent.left == p) {
            p.parent.left = x;
        } else {
            p.parent.right = x;
        }
        x.left = p;
        p.parent = x;
    }

    // Helper: Find max node in subtree
    private Node subtreeMax(Node x) {
        if (x == null) return null;
        while (x.right != null) x = x.right;
        return x;
    }
}