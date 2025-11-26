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
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                splay(z); // key already exists, splay it to root
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

        if (node == null) {
            return;
        }

        splay(node);

        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            maxLeft.right = node.right;
            if (node.right != null) {
                node.right.parent = maxLeft;
            }
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
        // Help GC
        node.left = node.right = node.parent = null;
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

    // Helper: Find node with given key
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

    // Helper: Splay operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag
                rightRotate(x.parent);
                leftRotate(x.parent);
            } else {
                // Zig-zag
                leftRotate(x.parent);
                rightRotate(x.parent);
            }
        }
        root = x;
    }

    // Helper: Right rotation
    private void rightRotate(Node y) {
        Node x = y.left;
        if (x == null) return;
        y.left = x.right;
        if (x.right != null) {
            x.right.parent = y;
        }
        x.parent = y.parent;
        if (y.parent == null) {
            root = x;
        } else if (y == y.parent.right) {
            y.parent.right = x;
        } else {
            y.parent.left = x;
        }
        x.right = y;
        y.parent = x;
    }

    // Helper: Left rotation
    private void leftRotate(Node y) {
        Node x = y.right;
        if (x == null) return;
        y.right = x.left;
        if (x.left != null) {
            x.left.parent = y;
        }
        x.parent = y.parent;
        if (y.parent == null) {
            root = x;
        } else if (y == y.parent.left) {
            y.parent.left = x;
        } else {
            y.parent.right = x;
        }
        x.left = y;
        y.parent = x;
    }

    // Helper: Find max in subtree
    private Node subtreeMax(Node x) {
        while (x.right != null) {
            x = x.right;
        }
        return x;
    }

    // Optional: For debugging, Print tree (in-order)
    // public void printInOrder() {
    //     printInOrder(root);
    //     System.out.println();
    // }

    // private void printInOrder(Node node) {
    //     if (node != null) {
    //         printInOrder(node.left);
    //         System.out.print(node.key + " ");
    //         printInOrder(node.right);
    //     }
    // }
}