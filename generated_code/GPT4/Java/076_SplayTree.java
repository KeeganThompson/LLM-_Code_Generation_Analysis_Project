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

    // Public method to insert a key
    public void insert(int key) {
        root = insert(root, key, null);
        return;
    }

    // Internal recursive insert that returns the new root of the subtree
    private Node insert(Node node, int key, Node parent) {
        if (node == null) {
            Node newNode = new Node(key, parent);
            splay(newNode);
            return newNode;
        }
        if (key < node.key) {
            node.left = insert(node.left, key, node);
        } else if (key > node.key) {
            node.right = insert(node.right, key, node);
        } else {
            // Duplicate keys not allowed; splay existing node
            splay(node);
            return node;
        }
        return node;
    }

    // Public method to delete a key
    public void delete(int key) {
        Node node = findNode(root, key);
        if (node == null) return;
        splay(node);
        if (node.left != null) {
            Node maxLeft = subtreeMax(node.left);
            splay(maxLeft);
            maxLeft.right = node.right;
            if (node.right != null) node.right.parent = maxLeft;
            root = maxLeft;
            maxLeft.parent = null;
        } else {
            root = node.right;
            if (root != null) root.parent = null;
        }
    }

    // Public method to search for a key and splay the accessed node
    public Integer search(int key) {
        Node node = root, last = null;
        while (node != null) {
            last = node;
            if (key < node.key) node = node.left;
            else if (key > node.key) node = node.right;
            else {
                splay(node);
                return node.key;
            }
        }
        if (last != null) splay(last);
        return null;
    }

    // Splaying operation
    private void splay(Node x) {
        if (x == null) return;
        while (x.parent != null) {
            if (x.parent.parent == null) {
                // Zig
                if (x.parent.left == x) {
                    rightRotate(x.parent);
                } else {
                    leftRotate(x.parent);
                }
            } else if (x.parent.left == x && x.parent.parent.left == x.parent) {
                // Zig-Zig (left-left)
                rightRotate(x.parent.parent);
                rightRotate(x.parent);
            } else if (x.parent.right == x && x.parent.parent.right == x.parent) {
                // Zig-Zig (right-right)
                leftRotate(x.parent.parent);
                leftRotate(x.parent);
            } else if (x.parent.left == x && x.parent.parent.right == x.parent) {
                // Zig-Zag (left-right)
                rightRotate(x.parent);
                leftRotate(x.parent);
            } else {
                // Zig-Zag (right-left)
                leftRotate(x.parent);
                rightRotate(x.parent);
            }
        }
        root = x;
    }

    // Left rotation
    private void leftRotate(Node x) {
        Node y = x.right;
        if (y == null) return;
        x.right = y.left;
        if (y.left != null) y.left.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x.parent.left == x) x.parent.left = y;
        else x.parent.right = y;
        y.left = x;
        x.parent = y;
    }

    // Right rotation
    private void rightRotate(Node x) {
        Node y = x.left;
        if (y == null) return;
        x.left = y.right;
        if (y.right != null) y.right.parent = x;
        y.parent = x.parent;
        if (x.parent == null) root = y;
        else if (x.parent.left == x) x.parent.left = y;
        else x.parent.right = y;
        y.right = x;
        x.parent = y;
    }

    // Helper to find a node by key
    private Node findNode(Node node, int key) {
        while (node != null) {
            if (key < node.key) node = node.left;
            else if (key > node.key) node = node.right;
            else return node;
        }
        return null;
    }

    // Helper to find the max node in a subtree
    private Node subtreeMax(Node node) {
        while (node.right != null) node = node.right;
        return node;
    }

    // Optional: For testing/debugging
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
}