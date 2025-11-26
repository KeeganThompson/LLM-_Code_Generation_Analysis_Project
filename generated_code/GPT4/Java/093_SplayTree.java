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

        while (z != null) {
            p = z;
            if (key < z.key)
                z = z.left;
            else if (key > z.key)
                z = z.right;
            else {
                splay(z);
                return; // Key already exists; do nothing
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
        if (node == null) return;

        splay(node);

        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            maxLeft.right = node.right;
            if (node.right != null) node.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            node.right.parent = null;
        } else {
            root = null;
        }

        // Help GC
        node.left = node.right = node.parent = null;
    }

    // Public search method. Returns Integer or null.
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Standard BST search (no splay)
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

    // Splaying operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step
                if (x.parent.left == x) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig step (left-left)
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig step (right-right)
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag step (left-right)
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-zag step (right-left)
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
        root = x;
    }

    // Rotate right at node y
    private void rotateRight(Node y) {
        Node x = y.left;
        if (x == null) return;
        y.left = x.right;
        if (x.right != null)
            x.right.parent = y;
        x.parent = y.parent;
        if (y.parent == null) {
            root = x;
        } else if (y == y.parent.left) {
            y.parent.left = x;
        } else {
            y.parent.right = x;
        }
        x.right = y;
        y.parent = x;
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

    // Helper: Find the maximum node in a subtree
    private Node subtreeMax(Node n) {
        while (n.right != null)
            n = n.right;
        return n;
    }

    // Optional: For debugging, print the tree
    public void printTree() {
        printTree(root, "", true);
    }

    private void printTree(Node node, String prefix, boolean isTail) {
        if (node == null) return;
        System.out.println(prefix + (isTail ? "└── " : "├── ") + node.key);
        if (node.left != null || node.right != null) {
            if (node.left != null)
                printTree(node.left, prefix + (isTail ? "    " : "│   "), false);
            if (node.right != null)
                printTree(node.right, prefix + (isTail ? "    " : "│   "), true);
        }
    }
}