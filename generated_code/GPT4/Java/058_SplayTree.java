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

    /**
     * Inserts the key into the set.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
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
                return; // Key already exists, do not insert duplicates
            }
        }
        Node n = new Node(key, p);
        if (key < p.key)
            p.left = n;
        else
            p.right = n;
        splay(n);
    }

    /**
     * Deletes the key from the set if it exists.
     */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return;
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
                if (min.right != null)
                    min.right.parent = min;
            }
            replace(node, min);
            min.left = node.left;
            if (min.left != null)
                min.left.parent = min;
        }
        node.left = node.right = node.parent = null; // Help GC
    }

    /**
     * Searches for the key in the set.
     * If found, returns the key (as Integer), else returns null.
     * The accessed node (or last accessed) is splayed to the root if any access occurred.
     */
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
            splay(last); // Splay the last accessed node
        return null;
    }

    // Helper: Find node by key (no splaying)
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

    // Helper: Replace u with v in the parent
    private void replace(Node u, Node v) {
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

    // Helper: Splay operation
    private void splay(Node x) {
        if (x == null)
            return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x == x.parent.left)
                    rotateRight(x.parent);
                else
                    rotateLeft(x.parent);
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-zig
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-zig
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-zag
                rotateLeft(x.parent);
                rotateRight(x.parent);
            } else {
                // Zig-zag
                rotateRight(x.parent);
                rotateLeft(x.parent);
            }
        }
    }

    // Left rotation at x
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

    // Right rotation at x
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

    // Helper: Find subtree minimum
    private Node subtreeMin(Node node) {
        while (node.left != null)
            node = node.left;
        return node;
    }

    // Optional: For debug
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        print(root, sb, "", "");
        return sb.toString();
    }

    private void print(Node n, StringBuilder sb, String prefix, String childrenPrefix) {
        if (n == null) return;
        sb.append(prefix);
        sb.append(n.key);
        sb.append('\n');
        if (n.right != null) {
            print(n.right, sb, childrenPrefix + "├── ", childrenPrefix + "│   ");
        }
        if (n.left != null) {
            print(n.left, sb, childrenPrefix + "└── ", childrenPrefix + "    ");
        }
    }
}