public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
            this.left = this.right = this.parent = null;
        }
    }

    private Node root;

    public SplayTree() {
        root = null;
    }

    // Public method to insert a key
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
                // Key already exists, splay it to the root
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

    // Public method to delete a key
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return;

        splay(node);

        // Now node is root
        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            // maxLeft is now root
            maxLeft.right = node.right;
            if (node.right != null)
                node.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
    }

    // Public method to search a key. Returns Integer or null.
    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with key, no splaying
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
        if (x == null)
            return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-Zig
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-Zig
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-Zag
                rightRotate(x.parent);
                leftRotate(x.parent);
            } else {
                // Zig-Zag
                leftRotate(x.parent);
                rightRotate(x.parent);
            }
        }
        root = x;
    }

    // Right rotate at y
    private void rightRotate(Node y) {
        Node x = y.left;
        if (x == null)
            return;
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

    // Left rotate at x
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null)
            return;
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

    // Helper: Find max node in subtree
    private Node subtreeMax(Node node) {
        while (node.right != null)
            node = node.right;
        return node;
    }

    // Optional: For testing/debugging
    // public void inorder() {
    //     inorder(root);
    //     System.out.println();
    // }
    // private void inorder(Node node) {
    //     if (node != null) {
    //         inorder(node.left);
    //         System.out.print(node.key + " ");
    //         inorder(node.right);
    //     }
    // }
}