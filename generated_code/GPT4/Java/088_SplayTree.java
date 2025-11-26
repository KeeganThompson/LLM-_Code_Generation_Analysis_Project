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
                return; // Key already in the set
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

        if (node.left == null) {
            transplant(node, node.right);
        } else if (node.right == null) {
            transplant(node, node.left);
        } else {
            Node min = subtreeMin(node.right);
            if (min.parent != node) {
                transplant(min, min.right);
                min.right = node.right;
                if (min.right != null)
                    min.right.parent = min;
            }
            transplant(node, min);
            min.left = node.left;
            if (min.left != null)
                min.left.parent = min;
        }
    }

    // Public search method
    // Returns Integer (boxed) or null if not found
    public Integer search(int key) {
        Node node = root;
        Node last = null;
        while (node != null) {
            last = node;
            if (key < node.key)
                node = node.left;
            else if (key > node.key)
                node = node.right;
            else {
                splay(node);
                return node.key;
            }
        }
        if (last != null)
            splay(last);
        return null;
    }

    // Helper: Find node with key
    private Node findNode(int key) {
        Node node = root;
        while (node != null) {
            if (key < node.key)
                node = node.left;
            else if (key > node.key)
                node = node.right;
            else
                return node;
        }
        return null;
    }

    // Helper: Splaying operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step
                if (x == x.parent.left) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-zig step
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-zig step
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-zag step
                leftRotate(x.parent);
                rightRotate(x.parent);
            } else {
                // Zig-zag step
                rightRotate(x.parent);
                leftRotate(x.parent);
            }
        }
        root = x;
    }

    // Helper: Left rotation
    private void leftRotate(Node x) {
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

    // Helper: Right rotation
    private void rightRotate(Node x) {
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

    // Helper: Replace subtree u with v
    private void transplant(Node u, Node v) {
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

    // Helper: Minimum of subtree
    private Node subtreeMin(Node x) {
        while (x.left != null)
            x = x.left;
        return x;
    }

    // Optional: For testing/debugging
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