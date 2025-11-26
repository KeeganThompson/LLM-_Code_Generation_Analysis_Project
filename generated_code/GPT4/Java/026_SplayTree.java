public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;
        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Right rotate x
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y != null) {
            x.left = y.right;
            if (y.right != null) y.right.parent = x;
            y.parent = x.parent;
        }
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        if (y != null) {
            y.right = x;
        }
        x.parent = y;
    }

    // Left rotate x
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y != null) {
            x.right = y.left;
            if (y.left != null) y.left.parent = x;
            y.parent = x.parent;
        }
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        if (y != null) {
            y.left = x;
        }
        x.parent = y;
    }

    // Splay node x to root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig step
                if (x.parent.left == x) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig step
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig step
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag step
                rightRotate(x.parent);
                leftRotate(x.parent);
            } else {
                // Zig-zag step
                leftRotate(x.parent);
                rightRotate(x.parent);
            }
        }
    }

    // Search for key and splay the accessed node to root
    public Integer search(int key) {
        Node z = root;
        Node last = null;
        while (z != null) {
            last = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                splay(z);
                return z.key;
            }
        }
        // Splay the last accessed node (parent of where key would be)
        if (last != null) {
            splay(last);
        }
        return null;
    }

    // Insert key into the set
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

    // Delete key from the set
    public void delete(int key) {
        Node node = root;
        while (node != null) {
            if (key < node.key) {
                node = node.left;
            } else if (key > node.key) {
                node = node.right;
            } else {
                break;
            }
        }
        if (node == null) {
            // Key not found
            return;
        }
        splay(node);
        if (node.left == null) {
            transplant(node, node.right);
        } else if (node.right == null) {
            transplant(node, node.left);
        } else {
            Node min = subtreeMin(node.right);
            if (min.parent != node) {
                transplant(min, min.right);
                min.right = node.right;
                if (min.right != null) min.right.parent = min;
            }
            transplant(node, min);
            min.left = node.left;
            if (min.left != null) min.left.parent = min;
        }
    }

    // Helper: subtree minimum
    private Node subtreeMin(Node x) {
        while (x.left != null) x = x.left;
        return x;
    }

    // Helper: transplant u with v in tree
    private void transplant(Node u, Node v) {
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

    // (Optional) For debugging: inorder traversal
    public void inorder() {
        inorder(root);
        System.out.println();
    }
    private void inorder(Node node) {
        if (node == null) return;
        inorder(node.left);
        System.out.print(node.key + " ");
        inorder(node.right);
    }

    // (Optional) For debugging: get root key
    public Integer getRootKey() {
        return root == null ? null : root.key;
    }

    // Main method for demonstration (You can remove this in production)
    public static void main(String[] args) {
        SplayTree tree = new SplayTree();
        tree.insert(10);
        tree.insert(20);
        tree.insert(30);
        tree.insert(40);
        tree.insert(50);
        tree.inorder(); // 10 20 30 40 50

        System.out.println(tree.search(30)); // 30, should splay 30 to root
        System.out.println("Root: " + tree.getRootKey()); // 30

        tree.delete(20);
        tree.inorder(); // 10 30 40 50

        System.out.println(tree.search(100)); // null
        tree.inorder();
    }
}