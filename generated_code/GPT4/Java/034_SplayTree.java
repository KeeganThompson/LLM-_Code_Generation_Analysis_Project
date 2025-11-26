public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;
        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    /**
     * Inserts key into the set. Does nothing if already present.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node z = root, p = null;
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                // Key already exists, splay it to root
                splay(z);
                return;
            }
        }
        Node n = new Node(key);
        n.parent = p;
        if (key < p.key) {
            p.left = n;
        } else {
            p.right = n;
        }
        splay(n);
    }

    /**
     * Deletes key from the set. Does nothing if not present.
     */
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) {
            return;
        }
        splay(node);
        // Now node is at root
        if (node.left == null) {
            replace(node, node.right);
        } else if (node.right == null) {
            replace(node, node.left);
        } else {
            // Both children exist
            Node min = subtreeMin(node.right);
            if (min.parent != node) {
                replace(min, min.right);
                min.right = node.right;
                if (min.right != null) {
                    min.right.parent = min;
                }
            }
            replace(node, min);
            min.left = node.left;
            if (min.left != null) {
                min.left.parent = min;
            }
        }
        node.left = node.right = node.parent = null; // Help GC
    }

    /**
     * Searches for key in the set. Splays the accessed node to the root if found.
     * Returns key if found, or null if not present.
     */
    public Integer search(int key) {
        Node node = root;
        Node last = null;
        while (node != null) {
            last = node;
            if (key < node.key) {
                node = node.left;
            } else if (key > node.key) {
                node = node.right;
            } else {
                splay(node);
                return node.key;
            }
        }
        if (last != null) {
            splay(last); // Splay the last accessed node
        }
        return null;
    }

    // --- Helper methods ---

    private Node findNode(int key) {
        Node node = root;
        while (node != null) {
            if (key < node.key) {
                node = node.left;
            } else if (key > node.key) {
                node = node.right;
            } else {
                return node;
            }
        }
        return null;
    }

    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig rotation
                if (x == x.parent.left) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-zig rotation
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-zig rotation
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-zag rotation
                leftRotate(x.parent);
                rightRotate(x.parent);
            } else {
                // Zig-zag rotation
                rightRotate(x.parent);
                leftRotate(x.parent);
            }
        }
        root = x;
    }

    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) {
            y.left.parent = x;
        }
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

    private void rightRotate(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) {
            y.right.parent = x;
        }
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

    private void replace(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null) {
            v.parent = u.parent;
        }
    }

    private Node subtreeMin(Node x) {
        while (x.left != null) {
            x = x.left;
        }
        return x;
    }

    // --- For debugging purposes only ---
    /*
    public void printTree() {
        printTree(root, "", true);
    }
    private void printTree(Node node, String prefix, boolean isTail) {
        if (node == null) return;
        System.out.println(prefix + (isTail ? "└── " : "├── ") + node.key);
        printTree(node.left, prefix + (isTail ? "    " : "│   "), false);
        printTree(node.right, prefix + (isTail ? "    " : "│   "), true);
    }
    */
}