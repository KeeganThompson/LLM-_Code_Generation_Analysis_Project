public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key, Node parent) {
            this.key = key;
            this.left = null;
            this.right = null;
            this.parent = parent;
        }
    }

    private Node root;

    public SplayTree() {
        this.root = null;
    }

    // Public insert method
    public void insert(int key) {
        if (root == null) {
            root = new Node(key, null);
            return;
        }
        Node z = root;
        Node p = null;
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                // Duplicate, do nothing
                splay(z);
                return;
            }
        }
        Node n = new Node(key, p);
        if (key < p.key) {
            p.left = n;
        } else {
            p.right = n;
        }
        splay(n);
    }

    // Public delete method
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) {
            return;
        }
        splay(node);
        // Now node is at root
        if (node.left != null) {
            Node maxLeft = subtreeMaximum(node.left);
            splay(maxLeft);
            // Now maxLeft is the root, its right is null
            maxLeft.right = node.right;
            if (node.right != null) {
                node.right.parent = maxLeft;
            }
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

    // Helper to find node by key, no splay
    private Node findNode(int key) {
        Node z = root;
        while (z != null) {
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                return z;
            }
        }
        return null;
    }

    // Splay operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x == x.parent.left) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x == x.parent.left && x.parent == x.parent.parent.left) {
                // Zig-Zig
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.right) {
                // Zig-Zig
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x == x.parent.right && x.parent == x.parent.parent.left) {
                // Zig-Zag
                leftRotate(x.parent);
                rightRotate(x.parent);
            } else if (x == x.parent.left && x.parent == x.parent.parent.right) {
                // Zig-Zag
                rightRotate(x.parent);
                leftRotate(x.parent);
            }
        }
        root = x;
    }

    // Left rotate
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

    // Right rotate
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

    // Find maximum node in subtree
    private Node subtreeMaximum(Node x) {
        while (x.right != null) {
            x = x.right;
        }
        return x;
    }

    // Optional: for debugging
    // public void printTree() {
    //     printTree(root, "", true);
    // }
    // private void printTree(Node node, String prefix, boolean isTail) {
    //     if (node == null) return;
    //     System.out.println(prefix + (isTail ? "└── " : "├── ") + node.key);
    //     if (node.left != null || node.right != null) {
    //         if (node.left != null) printTree(node.left, prefix + (isTail ? "    " : "│   "), node.right == null);
    //         if (node.right != null) printTree(node.right, prefix + (isTail ? "    " : "│   "), true);
    //     }
    // }
}