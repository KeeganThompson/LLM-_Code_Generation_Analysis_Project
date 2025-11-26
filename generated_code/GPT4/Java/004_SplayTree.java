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
                // Key already exists, splay it
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
            // maxLeft is now root, attach right subtree
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
        // node is now disconnected
    }

    // Public search method; returns Integer or null
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

    // ----------- Private helper methods ------------

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

    private Node subtreeMax(Node node) {
        while (node.right != null)
            node = node.right;
        return node;
    }

    // Splaying: brings node x to the root
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            Node p = x.parent;
            Node gp = p.parent;
            if (gp == null) {
                // Zig
                if (x == p.left)
                    rotateRight(p);
                else
                    rotateLeft(p);
            } else if (x == p.left && p == gp.left) {
                // Zig-Zig
                rotateRight(gp);
                rotateRight(p);
            } else if (x == p.right && p == gp.right) {
                // Zig-Zig
                rotateLeft(gp);
                rotateLeft(p);
            } else if (x == p.right && p == gp.left) {
                // Zig-Zag
                rotateLeft(p);
                rotateRight(gp);
            } else if (x == p.left && p == gp.right) {
                // Zig-Zag
                rotateRight(p);
                rotateLeft(gp);
            }
        }
        root = x;
    }

    // Left rotation at node x
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null)
            return;
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

    // Right rotation at node x
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null)
            return;
        x.left = y.right;
        if (y.right != null)
            y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null)
            root = y;
        else if (x == x.parent.left)
            x.parent.left = y;
        else
            x.parent.right = y;
        y.right = x;
        x.parent = y;
    }
}