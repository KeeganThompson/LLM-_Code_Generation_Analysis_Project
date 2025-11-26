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
        Node z = root, p = null;
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
        if (key < p.key)
            p.left = n;
        else
            p.right = n;
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

    // Helper: find node with key
    private Node findNode(int key) {
        Node z = root;
        Node last = null;
        while (z != null) {
            last = z;
            if (key < z.key)
                z = z.left;
            else if (key > z.key)
                z = z.right;
            else
                return z;
        }
        if (last != null)
            splay(last);
        return null;
    }

    // Helper: rotate node x up
    private void rotate(Node x) {
        Node p = x.parent;
        if (p == null)
            return;
        Node g = p.parent;

        if (p.left == x) {
            p.left = x.right;
            if (x.right != null)
                x.right.parent = p;
            x.right = p;
        } else {
            p.right = x.left;
            if (x.left != null)
                x.left.parent = p;
            x.left = p;
        }
        p.parent = x;
        x.parent = g;

        if (g != null) {
            if (g.left == p)
                g.left = x;
            else
                g.right = x;
        } else {
            root = x;
        }
    }

    // Splaying operation
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig
                rotate(x);
            } else if ((g.left == p && p.left == x) || (g.right == p && p.right == x)) {
                // Zig-zig
                rotate(p);
                rotate(x);
            } else {
                // Zig-zag
                rotate(x);
                rotate(x);
            }
        }
    }

    // Helper: find max node in subtree
    private Node subtreeMax(Node node) {
        while (node.right != null)
            node = node.right;
        return node;
    }

    // Optional: For testing, inorder traversal
    public void printInOrder() {
        printInOrder(root);
        System.out.println();
    }

    private void printInOrder(Node node) {
        if (node == null)
            return;
        printInOrder(node.left);
        System.out.print(node.key + " ");
        printInOrder(node.right);
    }

    // Optional: get root for testing
    public Integer getRoot() {
        return root != null ? root.key : null;
    }
}