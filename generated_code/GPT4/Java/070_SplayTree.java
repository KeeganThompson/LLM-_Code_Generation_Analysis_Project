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

    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
            return;
        }
        Node curr = root;
        Node parent = null;
        while (curr != null) {
            parent = curr;
            if (key < curr.key) {
                curr = curr.left;
            } else if (key > curr.key) {
                curr = curr.right;
            } else {
                splay(curr);
                return; // Key already present
            }
        }
        Node newNode = new Node(key, parent);
        if (key < parent.key) {
            parent.left = newNode;
        } else {
            parent.right = newNode;
        }
        splay(newNode);
    }

    public void delete(int key) {
        Node node = findNode(root, key);
        if (node == null)
            return;

        splay(node);

        if (node.left == null) {
            replace(node, node.right);
            root = node.right;
            if (root != null) root.parent = null;
        } else if (node.right == null) {
            replace(node, node.left);
            root = node.left;
            if (root != null) root.parent = null;
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
            root = min;
            root.parent = null;
        }
    }

    public Integer search(int key) {
        Node node = findNode(root, key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // --- Private helpers ---

    private Node findNode(Node curr, int key) {
        Node last = null;
        while (curr != null) {
            last = curr;
            if (key < curr.key) {
                curr = curr.left;
            } else if (key > curr.key) {
                curr = curr.right;
            } else {
                return curr;
            }
        }
        // Optional: splay last accessed node for failed search
        // if (last != null) splay(last);
        return null;
    }

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

    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
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

    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
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
        if (x == null) return null;
        while (x.left != null) {
            x = x.left;
        }
        return x;
    }

    // --- Optional: For debugging purposes ---

    // public void printTree() {
    //     printTree(root, "", true);
    // }
    // private void printTree(Node node, String prefix, boolean isTail) {
    //     if (node == null) return;
    //     System.out.println(prefix + (isTail ? "└── " : "├── ") + node.key);
    //     printTree(node.left, prefix + (isTail ? "    " : "│   "), false);
    //     printTree(node.right, prefix + (isTail ? "    " : "│   "), true);
    // }
}