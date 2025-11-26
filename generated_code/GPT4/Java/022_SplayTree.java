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
        Node z = root;
        Node p = null;
        while (z != null) {
            p = z;
            if (key < z.key) {
                z = z.left;
            } else if (key > z.key) {
                z = z.right;
            } else {
                splay(z); // Key already exists, just splay
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

    public void delete(int key) {
        Node node = find(root, key);
        if (node == null) return;
        splay(node);
        if (node.left != null) {
            Node maxLeft = subtreeMaximum(node.left);
            splay(maxLeft);
            maxLeft.right = node.right;
            if (node.right != null) node.right.parent = maxLeft;
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
        if (last != null) splay(last); // Splay last accessed node
        return null;
    }

    // --- Private utility methods ---

    private Node find(Node node, int key) {
        while (node != null) {
            if (key < node.key) node = node.left;
            else if (key > node.key) node = node.right;
            else return node;
        }
        return null;
    }

    private Node subtreeMaximum(Node node) {
        while (node.right != null) node = node.right;
        return node;
    }

    // Splaying operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            Node p = x.parent;
            Node g = p.parent;
            if (g == null) {
                // Zig step
                if (x == p.left) {
                    rightRotate(p);
                } else {
                    leftRotate(p);
                }
            } else if (x == p.left && p == g.left) {
                // Zig-zig step
                rightRotate(g);
                rightRotate(p);
            } else if (x == p.right && p == g.right) {
                // Zig-zig step
                leftRotate(g);
                leftRotate(p);
            } else if (x == p.right && p == g.left) {
                // Zig-zag step
                leftRotate(p);
                rightRotate(g);
            } else if (x == p.left && p == g.right) {
                // Zig-zag step
                rightRotate(p);
                leftRotate(g);
            }
        }
        root = x;
    }

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

    // --- Optional: For testing ---

    // In-order traversal for debugging
    public void printInOrder() {
        printInOrder(root);
        System.out.println();
    }

    private void printInOrder(Node node) {
        if (node == null) return;
        printInOrder(node.left);
        System.out.print(node.key + " ");
        printInOrder(node.right);
    }

    // Simple main for demonstration / testing
    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(30);
        st.insert(40);
        st.insert(50);
        st.printInOrder(); // 10 20 30 40 50

        System.out.println(st.search(30)); // 30 (should splay 30 to root)
        st.printInOrder(); // 10 20 30 40 50

        st.delete(40);
        st.printInOrder(); // 10 20 30 50

        System.out.println(st.search(100)); // null
    }
}