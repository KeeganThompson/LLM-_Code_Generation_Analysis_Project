public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Public method to insert a key
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
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
                splay(z); // Key already exists, splay it to root
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

    // Public method to delete a key
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

    // Public method to search for a key; splays found node to root
    public Integer search(int key) {
        Node node = find(root, key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper: Find node with given key
    private Node find(Node node, int key) {
        Node z = node;
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

    // Helper: Splay the given node to the root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x) {
                    rotateRight(x.parent);
                } else {
                    rotateLeft(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-Zig
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-Zig
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-Zag
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-Zag
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
        root = x;
    }

    // Helper: Left rotation
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

    // Helper: Right rotation
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        y.right = x;
        x.parent = y;
    }

    // Helper: Replace node u with v in tree
    private void replace(Node u, Node v) {
        if (u.parent == null) {
            root = v;
        } else if (u == u.parent.left) {
            u.parent.left = v;
        } else {
            u.parent.right = v;
        }
        if (v != null) v.parent = u.parent;
    }

    // Helper: Find minimum node in subtree
    private Node subtreeMin(Node node) {
        while (node.left != null) node = node.left;
        return node;
    }

    // --- Optional: For testing and debugging ---
    // In-order traversal
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

    // --- Main method for simple testing ---
    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(30);
        st.insert(25);
        st.insert(5);
        st.insert(1);

        System.out.print("Inorder after inserts: ");
        st.inorder();

        System.out.println("Search 25: " + st.search(25));
        System.out.print("Inorder after search 25: ");
        st.inorder();

        st.delete(20);
        System.out.print("Inorder after delete 20: ");
        st.inorder();

        System.out.println("Search 100: " + st.search(100)); // null
    }
}