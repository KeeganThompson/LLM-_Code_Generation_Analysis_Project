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
                return;
            }
        }
        z = new Node(key);
        z.parent = p;
        if (p == null) {
            root = z;
        } else if (key < p.key) {
            p.left = z;
        } else {
            p.right = z;
        }
        splay(z);
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
            // maxLeft is now root, attach right subtree
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

    // Helper: Find node (no splaying here)
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
                if (x.parent.left == x)
                    rotateRight(x.parent);
                else
                    rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-Zig step (left-left)
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-Zig step (right-right)
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-Zag step (left-right)
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-Zag step (right-left)
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
        root = x;
    }

    // Rotate left
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null)
            y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    // Rotate right
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.right)
            x.parent.right = y;
        else
            x.parent.left = y;
        y.right = x;
        x.parent = y;
    }

    // Helper: Find max node in a subtree
    private Node subtreeMax(Node x) {
        while (x.right != null)
            x = x.right;
        return x;
    }

    // Optional: For debugging, to print the tree (not required)
    // public void print() {
    //     printHelper(root, "", true);
    // }
    // private void printHelper(Node node, String prefix, boolean isTail) {
    //     if (node == null) return;
    //     System.out.println(prefix + (isTail ? "└── " : "├── ") + node.key);
    //     printHelper(node.left, prefix + (isTail ? "    " : "│   "), false);
    //     printHelper(node.right, prefix + (isTail ? "    " : "│   "), true);
    // }
}