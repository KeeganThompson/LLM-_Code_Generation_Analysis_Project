public class SplayTree {
    private class Node {
        int key;
        Node left, right, parent;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    public void insert(int key) {
        Node z = root;
        Node p = null;

        while (z != null) {
            p = z;
            if (key < z.key)
                z = z.left;
            else if (key > z.key)
                z = z.right;
            else
                return; // Key already in the set, do nothing
        }

        z = new Node(key);
        z.parent = p;

        if (p == null) {
            root = z;
        } else if (key < p.key) {
            p.left = z;
        } else {
            p.right = z;
        }

        splay(z);
    }

    public void delete(int key) {
        Node node = findNode(key);
        if (node == null)
            return; // Key not in set

        splay(node);

        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            maxLeft.right = node.right;
            if (node.right != null)
                node.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else if (node.right != null) {
            root = node.right;
            root.parent = null;
        } else {
            root = null;
        }
    }

    public Integer search(int key) {
        Node node = findNode(key);
        if (node != null) {
            splay(node);
            return node.key;
        }
        return null;
    }

    // Helper functions

    private Node findNode(int key) {
        Node z = root;
        while (z != null) {
            if (key < z.key)
                z = z.left;
            else if (key > z.key)
                z = z.right;
            else
                return z;
        }
        return null;
    }

    private Node subtreeMax(Node n) {
        while (n.right != null)
            n = n.right;
        return n;
    }

    private void splay(Node x) {
        if (x == null)
            return;
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
        root = x;
    }

    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null)
            return;
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

    private void rightRotate(Node x) {
        Node y = x.left;
        if (y == null)
            return;
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

    // Optional: for testing purposes, print in-order traversal
    public void printInOrder() {
        printInOrder(root);
        System.out.println();
    }
    private void printInOrder(Node n) {
        if (n == null) return;
        printInOrder(n.left);
        System.out.print(n.key + " ");
        printInOrder(n.right);
    }

    // Main method for basic testing
    public static void main(String[] args) {
        SplayTree set = new SplayTree();
        set.insert(10);
        set.insert(20);
        set.insert(5);
        set.insert(15);

        set.printInOrder(); // Should print 5 10 15 20

        System.out.println(set.search(15)); // 15, and 15 is now root
        set.printInOrder();

        set.delete(10);
        set.printInOrder(); // Should print 5 15 20

        System.out.println(set.search(99)); // null
    }
}