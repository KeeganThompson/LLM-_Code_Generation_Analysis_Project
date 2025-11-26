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
     * Inserts a key into the splay tree.
     * If the key already exists, it does nothing.
     */
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
                splay(z); // Splay the existing node
                return;   // No duplicates allowed
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
     * Deletes a key from the splay tree.
     * If the key does not exist, do nothing.
     */
    public void delete(int key) {
        Node node = find(root, key);
        if (node == null) return;
        splay(node);
        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            // maxLeft is now root of left subtree
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

    /**
     * Searches for a key in the splay tree.
     * If found, splays the node to the root and returns the key.
     * If not found, splays the last accessed node and returns null.
     */
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
        if (last != null) splay(last);
        return null;
    }

    // ====== Private helper methods ======

    private Node find(Node node, int key) {
        while (node != null) {
            if (key < node.key) node = node.left;
            else if (key > node.key) node = node.right;
            else return node;
        }
        return null;
    }

    private Node subtreeMax(Node node) {
        while (node.right != null) node = node.right;
        return node;
    }

    // Splay operation: moves node x to root
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig rotation
                if (x.parent.left == x) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-zig rotation
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-zig rotation
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-zag rotation
                rightRotate(x.parent);
                leftRotate(x.parent);
            } else {
                // Zig-zag rotation
                leftRotate(x.parent);
                rightRotate(x.parent);
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

    // Optional: for testing purposes
    /*
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
    */

    // Main method for demonstration (optional, remove if not needed)
    /*
    public static void main(String[] args) {
        SplayTree tree = new SplayTree();
        tree.insert(10);
        tree.insert(20);
        tree.insert(5);
        tree.printInOrder(); // 5 10 20

        System.out.println(tree.search(10)); // 10
        tree.printInOrder(); // 5 10 20

        tree.delete(10);
        tree.printInOrder(); // 5 20

        System.out.println(tree.search(15)); // null
        tree.printInOrder(); // 5 20
    }
    */
}