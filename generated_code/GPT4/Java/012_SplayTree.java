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
        Node x = root;
        Node p = null;
        while (x != null) {
            p = x;
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                // Key already exists; splay it
                splay(x);
                return;
            }
        }
        Node newNode = new Node(key);
        newNode.parent = p;
        if (key < p.key) {
            p.left = newNode;
        } else {
            p.right = newNode;
        }
        splay(newNode);
    }

    // Public delete method
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
    }

    // Public search method
    public Integer search(int key) {
        Node node = find(root, key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Internal find (without splaying)
    private Node find(Node x, int key) {
        while (x != null) {
            if (key < x.key) {
                x = x.left;
            } else if (key > x.key) {
                x = x.right;
            } else {
                return x;
            }
        }
        return null;
    }

    // Splay operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig
                if (x == p.left) {
                    rightRotate(p);
                } else {
                    leftRotate(p);
                }
            } else if (x == p.left && p == g.left) {
                // Zig-Zig
                rightRotate(g);
                rightRotate(p);
            } else if (x == p.right && p == g.right) {
                // Zig-Zig
                leftRotate(g);
                leftRotate(p);
            } else if (x == p.right && p == g.left) {
                // Zig-Zag
                leftRotate(p);
                rightRotate(g);
            } else if (x == p.left && p == g.right) {
                // Zig-Zag
                rightRotate(p);
                leftRotate(g);
            }
        }
        root = x;
    }

    // Replace node u with node v in tree
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

    // Left rotate at x
    private void leftRotate(Node x) {
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

    // Right rotate at x
    private void rightRotate(Node x) {
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

    // Subtree minimum
    private Node subtreeMin(Node x) {
        while (x.left != null) x = x.left;
        return x;
    }

    // Optional: For testing
    // public void printInOrder() {
    //     printInOrder(root);
    //     System.out.println();
    // }
    // private void printInOrder(Node node) {
    //     if (node == null) return;
    //     printInOrder(node.left);
    //     System.out.print(node.key + " ");
    //     printInOrder(node.right);
    // }
}