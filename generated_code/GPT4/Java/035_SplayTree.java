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
        Node z = root;
        Node p = null;

        // Standard BST insert
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                // Key already exists, splay it to root
                splay(z);
                return;
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

    // Public delete method
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return;

        splay(node);

        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            maxLeft.right = node.right;
            if (node.right != null)
                node.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            node.right.parent = null;
        } else {
            root = null;
        }
    }

    // Public search method
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with given key (no splay)
    private Node findNode(int key) {
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

    // Helper: Maximum node in subtree
    private Node subtreeMax(Node node) {
        while (node.right != null)
            node = node.right;
        return node;
    }

    // Splay operation
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step
                if (x == x.parent.left) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-Zig step
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-Zig step
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-Zag step
                leftRotate(x.parent);
                rightRotate(x.parent);
            } else {
                // Zig-Zag step
                rightRotate(x.parent);
                leftRotate(x.parent);
            }
        }
        root = x;
    }

    // Right rotation
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y != null) {
            x.left = y.right;
            if (y.right != null)
                y.right.parent = x;
            y.parent = x.parent;
        }

        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        if (y != null)
            y.right = x;
        x.parent = y;
    }

    // Left rotation
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y != null) {
            x.right = y.left;
            if (y.left != null)
                y.left.parent = x;
            y.parent = x.parent;
        }

        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        if (y != null)
            y.left = x;
        x.parent = y;
    }
}