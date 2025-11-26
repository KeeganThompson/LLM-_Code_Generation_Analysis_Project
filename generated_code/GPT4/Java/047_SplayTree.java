public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
            this.left = this.right = this.parent = null;
        }
    }

    private Node root;

    public SplayTree() {
        root = null;
    }

    // Right rotation
    private void rotateRight(Node x) {
        Node y = x.left;
        if (y != null) {
            x.left = y.right;
            if (y.right != null) {
                y.right.parent = x;
            }
            y.parent = x.parent;
        }

        if (x.parent == null) {
            root = y;
        } else if (x == x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        if (y != null) {
            y.right = x;
        }
        x.parent = y;
    }

    // Left rotation
    private void rotateLeft(Node x) {
        Node y = x.right;
        if (y != null) {
            x.right = y.left;
            if (y.left != null) {
                y.left.parent = x;
            }
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

    // Splay operation
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
                // Zig-zig
                rotateRight(x.parent.parent);
                rotateRight(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig
                rotateLeft(x.parent.parent);
                rotateLeft(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag
                rotateRight(x.parent);
                rotateLeft(x.parent);
            } else {
                // Zig-zag
                rotateLeft(x.parent);
                rotateRight(x.parent);
            }
        }
    }

    // Search and splay
    public Integer search(int key) {
        Node x = root;
        Node last = null;
        while (x != null) {
            last = x;
            if (key == x.key) {
                splay(x);
                return x.key;
            } else if (key < x.key) {
                x = x.left;
            } else {
                x = x.right;
            }
        }
        // Splay the last accessed node, if any
        if (last != null) splay(last);
        return null;
    }

    // Insert a key (no duplicates)
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        Node x = root;
        Node parent = null;
        while (x != null) {
            parent = x;
            if (key == x.key) {
                splay(x);
                return; // No duplicates
            } else if (key < x.key) {
                x = x.left;
            } else {
                x = x.right;
            }
        }
        Node node = new Node(key);
        node.parent = parent;
        if (key < parent.key) {
            parent.left = node;
        } else {
            parent.right = node;
        }
        splay(node);
    }

    // Delete a key
    public void delete(int key) {
        Node node = findNode(key);
        if (node == null) return;
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
        node.left = node.right = node.parent = null; // Help GC
    }

    // Utility: Replace u with v in the tree
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

    // Utility: Find node with given key
    private Node findNode(int key) {
        Node x = root;
        while (x != null) {
            if (key == x.key) {
                return x;
            } else if (key < x.key) {
                x = x.left;
            } else {
                x = x.right;
            }
        }
        return null;
    }

    // Utility: Minimum node in a subtree
    private Node subtreeMin(Node x) {
        if (x == null) return null;
        while (x.left != null) x = x.left;
        return x;
    }

    // (Optional) For debugging: inorder traversal
    public void printInOrder() {
        printInOrder(root);
        System.out.println();
    }

    private void printInOrder(Node x) {
        if (x == null) return;
        printInOrder(x.left);
        System.out.print(x.key + " ");
        printInOrder(x.right);
    }

    // Main for quick testing
    public static void main(String[] args) {
        SplayTree st = new SplayTree();
        st.insert(10);
        st.insert(20);
        st.insert(5);
        st.insert(8);
        st.printInOrder(); // 5 8 10 20

        System.out.println(st.search(8)); // 8
        st.printInOrder(); // (order unchanged)

        st.delete(10);
        st.printInOrder(); // 5 8 20

        System.out.println(st.search(100)); // null
    }
}