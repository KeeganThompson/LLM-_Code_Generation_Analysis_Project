public class SplayTree {
    private Node root;

    private static class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
        }
    }

    /**
     * Inserts the given key into the splay tree.
     * If the key already exists, does nothing.
     * @param key the key to insert
     */
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
        Node node = new Node(key);
        if (key < root.key) {
            node.right = root;
            node.left = root.left;
            root.left = null;
        } else { // key > root.key
            node.left = root;
            node.right = root.right;
            root.right = null;
        }
        root = node;
    }

    /**
     * Deletes the given key from the splay tree.
     * If the key does not exist, does nothing.
     * @param key the key to delete
     */
    public void delete(int key) {
        if (root == null) return;
        root = splay(root, key);
        if (root.key != key) {
            // Key not found, do nothing
            return;
        }
        if (root.left == null) {
            root = root.right;
        } else {
            Node temp = root.right;
            root = root.left;
            // Splay the maximum node in the left subtree to the root
            root = splay(root, key);
            root.right = temp;
        }
    }

    /**
     * Searches for the key in the splay tree, splays the accessed node to the root.
     * @param key the key to search for
     * @return the key if found, or null otherwise
     */
    public Integer search(int key) {
        if (root == null) return null;
        root = splay(root, key);
        if (root.key == key) {
            return root.key;
        }
        return null;
    }

    // Splay operation: brings the node with key 'key' to the root, or the last accessed node if not found
    private Node splay(Node node, int key) {
        if (node == null) return null;

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
        } else if (key > node.key) {
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
        } else {
            // key == node.key
            return node;
        }
    }

    private Node rotateRight(Node y) {
        Node x = y.left;
        if (x == null) return y;
        y.left = x.right;
        x.right = y;
        return x;
    }

    private Node rotateLeft(Node y) {
        Node x = y.right;
        if (x == null) return y;
        y.right = x.left;
        x.left = y;
        return x;
    }

    // Optional: For testing and debugging
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(Node node) {
        if (node != null) {
            inorder(node.left);
            System.out.print(node.key + " ");
            inorder(node.right);
        }
    }
}