public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key, Node parent) {
            this.key = key;
            this.parent = parent;
        }
    }

    private Node root;

    // Public insert
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
            return;
        }
        Node cur = root, parent = null;
        while (cur != null) {
            parent = cur;
            if (key < cur.key) cur = cur.left;
            else if (key > cur.key) cur = cur.right;
            else {
                splay(cur);  // Already exists, splay it.
                return;
            }
        }
        Node newNode = new Node(key, parent);
        if (key < parent.key) parent.left = newNode;
        else parent.right = newNode;
        splay(newNode);
    }

    // Public delete
    public void delete(int key) {
        Node node = find(root, key);
        if (node == null) return;
        splay(node);
        if (node.left == null) {
            replace(node, node.right);
        } else if (node.right == null) {
            replace(node, node.left);
        } else {
            Node min = subtreeMin(node.right);
            if (min.parent != node) {
                replace(min, min.right);
                min.right = node.right;
                if (min.right != null) min.right.parent = min;
            }
            replace(node, min);
            min.left = node.left;
            if (min.left != null) min.left.parent = min;
        }
        node.left = node.right = node.parent = null; // Help GC
    }

    // Public search
    public Integer search(int key) {
        Node node = find(root, key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // ---- Internal helpers ----

    // Splaying operation
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

    // Find node with key
    private Node find(Node node, int key) {
        while (node != null) {
            if (key < node.key) node = node.left;
            else if (key > node.key) node = node.right;
            else return node;
        }
        return null;
    }

    // Replace node u with node v in the tree
    private void replace(Node u, Node v) {
        if (u.parent == null) root = v;
        else if (u == u.parent.left) u.parent.left = v;
        else u.parent.right = v;
        if (v != null) v.parent = u.parent;
    }

    // Subtree minimum
    private Node subtreeMin(Node node) {
        while (node.left != null) node = node.left;
        return node;
    }

    // Left rotation at node x
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.left) x.parent.left = y;
        else x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    // Right rotation at node x
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x == x.parent.left) x.parent.left = y;
        else x.parent.right = y;
        y.right = x;
        x.parent = y;
    }
}