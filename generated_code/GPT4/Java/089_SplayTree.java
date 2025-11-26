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
                splay(z); // Duplicate, splay and return
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
        Node n = findNode(key);
        if (n == null)
            return;
        splay(n);

        if (n.left != null) {
            Node maxLeft = subtreeMaximum(n.left);
            splay(maxLeft);
            maxLeft.right = n.right;
            if (n.right != null)
                n.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else if (n.right != null) {
            root = n.right;
            root.parent = null;
        } else {
            root = null;
        }
    }

    // Public search method
    public Integer search(int key) {
        Node n = findNode(key);
        if (n != null) {
            splay(n);
            return n.key;
        }
        return null;
    }

    // Helper: Find node by key
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

    // Helper: Splay the node x to root
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step
                if (x.parent.left == x) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig step
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig step
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag step
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-zag step
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
        root = x;
    }

    // Rotate left at node x
    private void rotateLeft(Node x) {
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

    // Rotate right at node x
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null)
            return;
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

    // Helper: Subtree maximum
    private Node subtreeMaximum(Node x) {
        while (x.right != null)
            x = x.right;
        return x;
    }

    // Optional: For debugging; not required by prompt
    // public void inorder() {
    //     inorder(root);
    //     System.out.println();
    // }
    // private void inorder(Node n) {
    //     if (n == null)
    //         return;
    //     inorder(n.left);
    //     System.out.print(n.key + " ");
    //     inorder(n.right);
    // }
}