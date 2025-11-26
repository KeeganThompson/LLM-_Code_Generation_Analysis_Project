public class SplayTree {
    private class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Public method: Insert a key into the set
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        root = splay(root, key);
        if (root.key == key) {
            // Key already exists, do nothing
            return;
        }
        Node newNode = new Node(key);
        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
        } else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
        }
        root = newNode;
    }

    // Public method: Delete a key from the set
    public void delete(int key) {
        if (root == null)
            return;
        root = splay(root, key);
        if (root.key != key) {
            // Key not found, do nothing
            return;
        }
        if (root.left == null) {
            root = root.right;
        } else {
            Node temp = root.right;
            root = splay(root.left, key);
            root.right = temp;
        }
    }

    // Public method: Search for a key and splay it to the root
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return root.key;
        }
        return null;
    }

    // Splay operation: brings the node with given key to the root
    private Node splay(Node node, int key) {
        if (node == null || node.key == key)
            return node;

        if (key < node.key) {
            if (node.left == null) return node;
            if (key < node.left.key) {
                // Zig-Zig (Left Left)
                node.left.left = splay(node.left.left, key);
                node = rotateRight(node);
            } else if (key > node.left.key) {
                // Zig-Zag (Left Right)
                node.left.right = splay(node.left.right, key);
                if (node.left.right != null)
                    node.left = rotateLeft(node.left);
            }
            return (node.left == null) ? node : rotateRight(node);
        } else {
            if (node.right == null) return node;
            if (key > node.right.key) {
                // Zig-Zig (Right Right)
                node.right.right = splay(node.right.right, key);
                node = rotateLeft(node);
            } else if (key < node.right.key) {
                // Zig-Zag (Right Left)
                node.right.left = splay(node.right.left, key);
                if (node.right.left != null)
                    node.right = rotateRight(node.right);
            }
            return (node.right == null) ? node : rotateLeft(node);
        }
    }

    private Node rotateRight(Node x) {
        if (x == null || x.left == null) return x;
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    private Node rotateLeft(Node x) {
        if (x == null || x.right == null) return x;
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // Optionally, you may add a public method to print the tree for debugging
    // public void printTree() {
    //     printTree(root, "", true);
    // }

    // private void printTree(Node node, String prefix, boolean isTail) {
    //     if (node != null) {
    //         System.out.println(prefix + (isTail ? "└── " : "├── ") + node.key);
    //         printTree(node.left, prefix + (isTail ? "    " : "│   "), false);
    //         printTree(node.right, prefix + (isTail ? "    " : "│   "), true);
    //     }
    // }
}