public class SplayTree {
    private class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    /**
     * Splay operation: brings the node with the given key to the root.
     * If the key is not found, brings the last accessed node to the root.
     */
    private Node splay(Node root, int key) {
        if (root == null || root.key == key)
            return root;

        // Key lies in left subtree
        if (key < root.key) {
            if (root.left == null)
                return root;

            // Zig-Zig (Left Left)
            if (key < root.left.key) {
                root.left.left = splay(root.left.left, key);
                root = rotateRight(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                root.left.right = splay(root.left.right, key);

                if (root.left.right != null)
                    root.left = rotateLeft(root.left);
            }

            return (root.left == null) ? root : rotateRight(root);
        }
        // Key lies in right subtree
        else {
            if (root.right == null)
                return root;

            // Zag-Zig (Right Left)
            if (key < root.right.key) {
                root.right.left = splay(root.right.left, key);

                if (root.right.left != null)
                    root.right = rotateRight(root.right);
            }
            // Zag-Zag (Right Right)
            else if (key > root.right.key) {
                root.right.right = splay(root.right.right, key);
                root = rotateLeft(root);
            }

            return (root.right == null) ? root : rotateLeft(root);
        }
    }

    // Right rotation
    private Node rotateRight(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    // Left rotation
    private Node rotateLeft(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    /**
     * Insert key into the SplayTree. If key already exists, do nothing.
     */
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }

        root = splay(root, key);

        if (root.key == key) {
            // Key already in tree, do nothing
            return;
        }

        Node newNode = new Node(key);

        if (key < root.key) {
            newNode.right = root;
            newNode.left = root.left;
            root.left = null;
            root = newNode;
        } else {
            newNode.left = root;
            newNode.right = root.right;
            root.right = null;
            root = newNode;
        }
    }

    /**
     * Delete key from the SplayTree. If key not present, do nothing.
     */
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
            // Splay to bring the max node of left subtree as new root
            root = splay(root.left, key);
            root.right = temp;
        }
    }

    /**
     * Search for key in the SplayTree. Splays the accessed/found node to root.
     * @param key the key to search for
     * @return the key if found, otherwise null
     */
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key)
            return root.key;
        return null;
    }

    // Optional: For testing and debugging
    // public void printTree() {
    //     printTree(root, "", false);
    // }

    // private void printTree(Node node, String prefix, boolean isLeft) {
    //     if (node != null) {
    //         System.out.println(prefix + (isLeft ? "├── " : "└── ") + node.key);
    //         printTree(node.left, prefix + (isLeft ? "│   " : "    "), true);
    //         printTree(node.right, prefix + (isLeft ? "│   " : "    "), false);
    //     }
    // }
}