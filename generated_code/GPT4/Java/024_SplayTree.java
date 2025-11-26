public class SplayTree {
    private class Node {
        int key;
        Node left, right;

        Node(int key) {
            this.key = key;
        }
    }

    private Node root;

    // Splay operation: moves the node with the given key to the root (or the last accessed node)
    private Node splay(Node root, int key) {
        if (root == null || root.key == key) {
            return root;
        }

        // Key lies in left subtree
        if (key < root.key) {
            if (root.left == null) return root;

            // Zig-Zig (Left Left)
            if (key < root.left.key) {
                // First recursively bring the key as root of left-left
                root.left.left = splay(root.left.left, key);
                // First rotation for root
                root = rightRotate(root);
            }
            // Zig-Zag (Left Right)
            else if (key > root.left.key) {
                // Bring the key as root of left-right
                root.left.right = splay(root.left.right, key);
                // If left-right child exists, do first rotation
                if (root.left.right != null) {
                    root.left = leftRotate(root.left);
                }
            }

            // Second rotation for root
            return (root.left == null) ? root : rightRotate(root);
        }
        // Key lies in right subtree
        else {
            if (root.right == null) return root;

            // Zag-Zig (Right Left)
            if (key < root.right.key) {
                // Bring the key as root of right-left
                root.right.left = splay(root.right.left, key);
                // If right-left child exists, do first rotation
                if (root.right.left != null) {
                    root.right = rightRotate(root.right);
                }
            }
            // Zag-Zag (Right Right)
            else if (key > root.right.key) {
                // Bring the key as root of right-right
                root.right.right = splay(root.right.right, key);
                root = leftRotate(root);
            }

            // Second rotation for root
            return (root.right == null) ? root : leftRotate(root);
        }
    }

    // Right rotate
    private Node rightRotate(Node x) {
        Node y = x.left;
        x.left = y.right;
        y.right = x;
        return y;
    }

    // Left rotate
    private Node leftRotate(Node x) {
        Node y = x.right;
        x.right = y.left;
        y.left = x;
        return y;
    }

    // Public insert method
    public void insert(int key) {
        if (root == null) {
            root = new Node(key);
            return;
        }
        root = splay(root, key);
        if (root.key == key) {
            // Key already exists, do nothing (set does not allow duplicates)
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

    // Public delete method
    public void delete(int key) {
        if (root == null) return;
        root = splay(root, key);
        if (root.key != key) return; // Key not found

        // Now root.key == key
        if (root.left == null) {
            root = root.right;
        } else {
            Node temp = root.right;
            root = root.left;
            // Splay the maximum node in the left subtree to the root
            root = splay(root, key);
            // Attach the right subtree
            root.right = temp;
        }
    }

    // Public search method. Returns Integer key if found, else null
    public Integer search(int key) {
        root = splay(root, key);
        if (root != null && root.key == key) {
            return root.key;
        }
        return null;
    }

    // Optional: For testing. In-order traversal
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
}