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
                // Duplicate key, do nothing (set semantics)
                search(key); // Splay existing key to root
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
        Node node = searchNode(key);
        if (node == null) {
            return; // Key not found, nothing to delete
        }

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

    // Public search method
    public Integer search(int key) {
        Node node = searchNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // --- Internal helper methods ---

    // Splay the node to the root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node gp = p.parent;
            if (gp == null) {
                // Zig step
                if (x == p.left) {
                    rightRotate(p);
                } else {
                    leftRotate(p);
                }
            } else if (x == p.left && p == gp.left) {
                // Zig-Zig step (left-left)
                rightRotate(gp);
                rightRotate(p);
            } else if (x == p.right && p == gp.right) {
                // Zig-Zig step (right-right)
                leftRotate(gp);
                leftRotate(p);
            } else if (x == p.right && p == gp.left) {
                // Zig-Zag step (left-right)
                leftRotate(p);
                rightRotate(gp);
            } else if (x == p.left && p == gp.right) {
                // Zig-Zag step (right-left)
                rightRotate(p);
                leftRotate(gp);
            }
        }
        root = x;
    }

    // Left rotate at node x
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null) return;
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

    // Right rotate at node x
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y == null) return;
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

    // Replace node u with node v in the tree
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

    // Search for a node with a given key, no splaying
    private Node searchNode(int key) {
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

    // Find min node in subtree
    private Node subtreeMin(Node x) {
        while (x.left != null) {
            x = x.left;
        }
        return x;
    }

    // --- Optionally, you can add traversal or size methods for debugging ---
    // For demonstration purposes only.
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